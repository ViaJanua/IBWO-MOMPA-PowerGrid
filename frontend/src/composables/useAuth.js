import { ref, computed, watch } from 'vue';

// 全局单例用户状态
const user = ref(null);
const token = ref(localStorage.getItem('token') || null);

// 初始化时从 localStorage 读取用户信息
const initUser = () => {
  const stored = localStorage.getItem('user');
  if (stored) {
    try {
      const parsed = JSON.parse(stored);
      if (parsed && typeof parsed === 'object' && parsed.account) {
        user.value = parsed;
      } else {
        localStorage.removeItem('user');
        user.value = null;
      }
    } catch (e) {
      localStorage.removeItem('user');
      user.value = null;
    }
  }
};
initUser();

// 监听 token 变化自动存 localStorage
watch(token, (newToken) => {
  if (newToken) {
    localStorage.setItem('token', newToken);
  } else {
    localStorage.removeItem('token');
  }
}, { immediate: true });

// 监听 user 变化自动存 localStorage
watch(user, (newUser) => {
  if (newUser) {
    localStorage.setItem('user', JSON.stringify(newUser));
  } else {
    localStorage.removeItem('user');
  }
}, { deep: true, flush: 'post' });

export const useAuth = () => {
  const isLoggedIn = computed(() => !!token.value && !!user.value);

  const storeUser = (userData, userToken) => {
    token.value = userToken;
    user.value = { ...userData };
  };

  const logout = () => {
    token.value = null;
    user.value = null;
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    sessionStorage.clear();
  };

  return {
    user,
    token,
    isLoggedIn,
    storeUser,
    logout,
  };
};