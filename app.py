from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import pandas as pd
from pathlib import Path
import os
import sqlite3
from datetime import timedelta
import sys
from coordinated_dispatch import run, Settings

sys.path.insert(0, str(Path(__file__).parent))


from coordinated_dispatch import run, Settings

app = Flask(__name__, static_folder='.')
CORS(app)

# JWT 配置 
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
jwt = JWTManager(app)

# 头像上传配置 
UPLOAD_FOLDER = Path(__file__).parent / 'uploads'
UPLOAD_FOLDER.mkdir(exist_ok=True)
app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 头像静态资源访问
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    if not allowed_file(filename):
        return jsonify({"error": "非法文件格式"}), 400
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# 数据库初始化
DB_PATH = Path(__file__).parent / 'users'


def get_db_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            avatar TEXT,
            nickname TEXT
        )
    ''')
    cursor = conn.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cursor.fetchall()]
    if 'nickname' not in columns:
        conn.execute('ALTER TABLE users ADD COLUMN nickname TEXT')
    conn.commit()
    conn.close()


init_db()


# 注册 API 
@app.route('/api/auth/register', methods=['POST'])
def register():
    account = request.form.get('account')
    password = request.form.get('password')
    nickname = request.form.get('nickname', '').strip()
    if not account or not password:
        return jsonify({'error': '账号和密码不能为空'}), 400
    if not nickname:
        nickname = account
    conn = get_db_connection()
    existing = conn.execute('SELECT id FROM users WHERE account = ?', (account,)).fetchone()
    if existing:
        conn.close()
        return jsonify({'error': '该账号已被注册'}), 400
    avatar_filename = None
    if 'avatar' in request.files:
        file = request.files['avatar']
        if file.filename == '':
            conn.close()
            return jsonify({'error': '未选择头像文件'}), 400
        if not allowed_file(file.filename):
            conn.close()
            return jsonify({'error': '头像仅支持 png、jpg、jpeg、gif 格式'}), 400
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        timestamp = int(pd.Timestamp.now().timestamp())
        avatar_filename = f"{name}_{timestamp}{ext}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], avatar_filename))
    password_hash = generate_password_hash(password)
    conn.execute(
        'INSERT INTO users (account, password_hash, avatar, nickname) VALUES (?, ?, ?, ?)',
        (account, password_hash, avatar_filename, nickname)
    )
    conn.commit()
    conn.close()
    return jsonify({
        'message': '注册成功',
        'account': account,
        'nickname': nickname,
        'avatar': avatar_filename
    }), 201


# 登录 API 
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    account = data.get('account')
    password = data.get('password')
    if not account or not password:
        return jsonify({"error": "账号密码不能为空"}), 400
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE account = ?", (account,)).fetchone()
    conn.close()
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "账号或密码错误"}), 400
    token = create_access_token(identity=str(user["id"]))
    user_info = {
        "id": user["id"],
        "account": user["account"],
        "nickname": user["nickname"],
        "avatar": user["avatar"]
    }
    return jsonify({"token": token, "user": user_info})


# 获取当前用户信息
@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    user = conn.execute('SELECT id, account, avatar, nickname FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    return jsonify(dict(user)), 200


# 调度数据接口（读取预计算 CSV）
DATA_DIR = Path(__file__).parent / 'data'


@app.route('/api/scenes')
def get_scenes():
    summary_files = list(DATA_DIR.glob('*_场景汇总指标.csv'))
    scenes = []
    for f in summary_files:
        name = f.stem.replace('_场景汇总指标', '')
        scenes.append(name)
    return jsonify({'scenes': sorted(scenes)})


@app.route('/api/data')
def get_data():
    season = request.args.get('season', 'spring')
    penetration = request.args.get('penetration', '15%')
    scene_name = f"{season}_{penetration}"
    summary_path = DATA_DIR / f"{scene_name}_场景汇总指标.csv"
    if not summary_path.exists():
        return jsonify({'error': f'场景 {scene_name} 不存在'}), 404
    summary = pd.read_csv(summary_path).iloc[0].to_dict()
    hourly_path = DATA_DIR / f"{scene_name}_逐时调度数据.csv"
    hourly = pd.read_csv(hourly_path).to_dict(orient='records')
    result = {
        'scene': scene_name,
        'summary': {
            '日总购电成本': f"{summary.get('日总购电成本(元)', 0):.2f}",
            '网损降低率': f"{summary.get('网损降低率(%)', 0):.2f}",
            '电压合格率': f"{summary.get('电压合格率', 0) * 100:.1f}",
            '峰谷差削减率': f"{summary.get('峰谷差削减率(%)', 0):.2f}"
        },
        'hourly': hourly
    }
    return jsonify(result)


@app.route('/api/all-scenes')
def get_all_scenes():
    results = []
    for season in ['spring', 'summer', 'autumn', 'winter']:
        for pen in ['0%', '5%', '10%', '15%']:
            path = DATA_DIR / f"{season}_{pen}_场景汇总指标.csv"
            if path.exists():
                df = pd.read_csv(path)
                results.append(df.iloc[0].to_dict())
    return jsonify(results)


# 算法实时调度接口
@app.route('/api/run_algorithm', methods=['POST'])
def run_algorithm():

    try:
        #接收前端参数
        data = request.get_json()
        season = data.get('season', 'autumn')
        penetration = data.get('penetration', '15%')
        mode = data.get('mode', 'fast')  # 默认极速模式

        print(f"🔄 开始运行算法: {season} {penetration} (模式: {mode})")

        #根据模式配置算法参数
        if mode == 'fast':
            # 极速版
            cfg = Settings(
                season=season,
                penetration=penetration,
                seed=20260731,
                mompa_pop=3,
                mompa_iter=1,
                outer_iter=1
            )
        else:
            # 精确版
            cfg = Settings(
                season=season,
                penetration=penetration,
                seed=20260731,
                mompa_pop=6,
                mompa_iter=3,
                outer_iter=3
            )

        # 运行算法
        result_df = run(cfg)

        # 读取生成数据
        data_dir = Path(__file__).parent / 'data'
        hourly_path = data_dir / f"{season}_{penetration}_逐时调度数据.csv"
        summary_path = data_dir / f"{season}_{penetration}_场景汇总指标.csv"

        if not hourly_path.exists():
            return jsonify({'error': '算法运行成功但数据文件未生成'}), 500

        # 读取并转换为前端需要格式
        hourly_df = pd.read_csv(hourly_path)
        summary_df = pd.read_csv(summary_path)

        summary = {
            '日总购电成本': f"{summary_df.iloc[0]['日总购电成本(元)']:.2f}",
            '网损降低率': f"{summary_df.iloc[0]['网损降低率(%)']:.2f}",
            '电压合格率': f"{summary_df.iloc[0]['电压合格率'] * 100:.1f}",
            '峰谷差削减率': f"{summary_df.iloc[0]['峰谷差削减率(%)']:.2f}"
        }

        hourly = hourly_df.to_dict(orient='records')

        print(f"算法运行完成: {season} {penetration} (模式: {mode})")

        return jsonify({
            'scene': f"{season}_{penetration}",
            'summary': summary,
            'hourly': hourly
        })

    except Exception as e:
        print(f"算法运行失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'算法运行失败: {str(e)}'}), 500


# 前端路由
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path.startswith("api/") or path.startswith("uploads/"):
        return jsonify({"error": "资源不存在"}), 404
    return send_from_directory('.', 'frontend/index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)