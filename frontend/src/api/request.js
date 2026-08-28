// 统一API请求封装
const BASE_URL = '';

export const request = async (url, options = {}) => {
  const token = localStorage.getItem('token');
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const config = {
    ...options,
    headers,
  };

  if (options.body instanceof FormData) {
    delete headers['Content-Type'];
  }

  const response = await fetch(BASE_URL + url, config);
  const data = await response.json();

  if (!response.ok) {
    if (response.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    throw new Error(data.error || '请求失败');
  }
  return data;
};