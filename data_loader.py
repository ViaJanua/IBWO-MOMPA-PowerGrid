import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
CACHE_DIR = DATA_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)

FILE_MAP = {"0%": "electric_zero.xlsx", "5%": "electric_five.xlsx",
            "10%": "electric_ten.xlsx", "15%": "electric_fifteen.xlsx"}
SEASON_COLUMN = {"spring": 1, "summer": 2, "autumn": 3, "winter": 4}


def load_season_data(season="autumn", penetration="5%"):
    if season not in SEASON_COLUMN:
        raise ValueError(f"Unknown season: {season}")
    if penetration not in FILE_MAP:
        raise ValueError(f"Unknown penetration: {penetration}")


    cache_path = CACHE_DIR / f"{season}_{penetration}.pkl"

    if cache_path.exists():
        full_df = pd.read_pickle(cache_path)
    else:
        raw = pd.read_excel(DATA_DIR / FILE_MAP[penetration], header=None)
        sl = slice(2, 26)
        full_df = raw.iloc[sl, :]
        full_df.to_pickle(cache_path, protocol=5)

    season_col = SEASON_COLUMN[season]
    numeric = lambda column: pd.to_numeric(full_df.iloc[:, column], errors="raise").to_numpy(float)

    load = numeric(season_col)
    wt = numeric(season_col + 6)
    pv = numeric(season_col + 12)


    price_cache = CACHE_DIR / "price.pkl"
    if price_cache.exists():
        price = pd.read_pickle(price_cache)
    else:
        price_raw = pd.read_excel(DATA_DIR / "四个典型日数据.xlsx", sheet_name="电价")
        price = pd.to_numeric(price_raw.iloc[:24, 0], errors="raise").to_numpy(float)
        pd.Series(price).to_pickle(price_cache)

    return {"load": load, "wt": wt, "pv": pv, "price": price}
if __name__ == '__main__':
    print("开始加载数据")
    data = load_season_data(season='spring', penetration='0%')
    print("数据加载完成")