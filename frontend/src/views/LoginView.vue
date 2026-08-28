<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-box">
        <div class="back-home">
          <router-link to="/" class="back-btn">← 返回首页</router-link>
        </div>

        <div class="login-header">
          <span class="logo-icon"></span>
          <h1>智能电网实时模拟平台</h1>
          <p>{{ auth.isLoggedIn ? '个人中心' : (isLogin ? '登录' : '注册新用户') }}</p>
        </div>

        <!-- 未登录：显示 登录/注册 -->
        <template v-if="!auth.isLoggedIn">
          <div class="tab-bar">
            <button :class="['tab-btn', { active: isLogin }]" @click="isLogin = true">登录</button>
            <button :class="['tab-btn', { active: !isLogin }]" @click="isLogin = false">注册</button>
          </div>

          <!-- 登录表单 -->
          <form v-if="isLogin" @submit.prevent="handleLogin">
            <div class="form-group">
              <label>账号</label>
              <input type="text" v-model="loginAccount" placeholder="请输入手机号或邮箱" required />
            </div>
            <div class="form-group">
              <label>密码</label>
              <input type="password" v-model="loginPassword" placeholder="请输入密码" required />
            </div>
            <button type="submit" class="btn-primary full-width" :disabled="loading">
              {{ loading ? '登录中...' : '登录' }}
            </button>
            <div v-if="loginError" class="error-msg">{{ loginError }}</div>
          </form>

          <!-- 注册表单 -->
          <form v-else @submit.prevent="handleRegister">
            <div class="form-group">
              <label>账号</label>
              <input type="text" v-model="regAccount" placeholder="请设置账号" required />
            </div>
            <div class="form-group">
              <label>昵称</label>
              <input type="text" v-model="regNickname" placeholder="默认为账号名" />
            </div>
            <div class="form-group">
              <label>密码</label>
              <input type="password" v-model="regPassword" placeholder="至少6位" required minlength="6" />
            </div>
            <div class="form-group">
              <label>确认密码</label>
              <input type="password" v-model="regConfirm" placeholder="再次输入" required />
            </div>
            <button type="submit" class="btn-primary full-width" :disabled="loading">
              {{ loading ? '注册中...' : '立即注册' }}
            </button>
            <div v-if="regError" class="error-msg">{{ regError }}</div>
          </form>
        </template>

        <!-- 已登录：个人中心 -->
        <template v-else>
          <div class="profile-area">
            <div class="avatar-fixed">👤</div>
            <div class="info-line">
              <span class="label">昵称</span>
              <span class="value">{{ auth.user?.nickname || auth.user?.account }}</span>
            </div>
            <button class="btn-danger full-width" @click="handleLogout">退出登录</button>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { loginAPI, registerAPI } from '@/api/auth';
import { useAuth } from '@/composables/useAuth';

const router = useRouter();
const auth = useAuth();

const isLogin = ref(true);
const loading = ref(false);

// 登录表单
const loginAccount = ref('');
const loginPassword = ref('');
const loginError = ref('');

// 注册表单
const regAccount = ref('');
const regPassword = ref('');
const regConfirm = ref('');
const regNickname = ref('');
const regError = ref('');

// 登录
const handleLogin = async () => {
  loginError.value = '';
  loading.value = true;
  try {
    const data = await loginAPI(loginAccount.value, loginPassword.value);
    auth.storeUser(data.user, data.token);
    router.push('/');
  } catch (err) {
    loginError.value = err.message || '登录失败';
  } finally {
    loading.value = false;
  }
};

// 注册
const handleRegister = async () => {
  regError.value = '';
  if (regPassword.value !== regConfirm.value) {
    regError.value = '两次密码输入不一致';
    return;
  }
  loading.value = true;
  const formData = new FormData();
  formData.append('account', regAccount.value);
  formData.append('password', regPassword.value);
  formData.append('nickname', regNickname.value || regAccount.value);
  // 不传头像，后端默认 NULL
  try {
    await registerAPI(formData);
    alert('注册成功，请登录');
    // 切到登录并填入账号
    isLogin.value = true;
    loginAccount.value = regAccount.value;
    loginPassword.value = '';
    // 清空注册字段
    regAccount.value = '';
    regPassword.value = '';
    regConfirm.value = '';
    regNickname.value = '';
  } catch (err) {
    regError.value = err.message || '注册失败';
  } finally {
    loading.value = false;
  }
};

// 退出
const handleLogout = () => {
  auth.logout();
  window.location.href = '/login';
};
</script>

<style scoped>

.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #0a1628 0%, #1a365d 100%);
}
.login-container {
  width: 100%;
  max-width: 400px;
  padding: 20px;
}
.login-box {
  background: white;
  border-radius: 16px;
  padding: 32px 28px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}
.back-home {
  margin-bottom: 16px;
}
.back-btn {
  color: #2b6cb0;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
}
.back-btn:hover {
  text-decoration: underline;
}
.login-header {
  text-align: center;
  margin-bottom: 24px;
}
.login-header .logo-icon {
  font-size: 40px;
  display: block;
}
.login-header h1 {
  font-size: 22px;
  color: #0a1628;
  margin: 8px 0 4px;
}
.login-header p {
  color: #6b7a8f;
  font-size: 14px;
}
.tab-bar {
  display: flex;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  margin-bottom: 24px;
}
.tab-btn {
  flex: 1;
  padding: 10px 0;
  border: none;
  background: #f7fafc;
  font-size: 15px;
  cursor: pointer;
}
.tab-btn.active {
  background: #2b6cb0;
  color: white;
}
.form-group {
  margin-bottom: 16px;
}
.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 4px;
}
.form-group input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d0d7de;
  border-radius: 6px;
  font-size: 14px;
  outline: none;
  box-sizing: border-box;
}
.form-group input:focus {
  border-color: #2b6cb0;
}
.btn-primary {
  background: #2b6cb0;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 12px;
  font-size: 15px;
  cursor: pointer;
  width: 100%;
}
.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.btn-danger {
  background: #e53e3e;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 12px;
  font-size: 15px;
  cursor: pointer;
  width: 100%;
}
.error-msg {
  color: #e53e3e;
  font-size: 14px;
  margin-top: 12px;
  text-align: center;
}
.profile-area {
  text-align: center;
  padding: 10px 0;
}
.avatar-fixed {
  font-size: 80px;
  margin: 0 auto 20px;
  background: #edf2f7;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.info-line {
  font-size: 18px;
  margin-bottom: 30px;
}
.info-line .label {
  color: #6b7a8f;
  margin-right: 10px;
}
.info-line .value {
  font-weight: 600;
  color: #0a1628;
}
</style>