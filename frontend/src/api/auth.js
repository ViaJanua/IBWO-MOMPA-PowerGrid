import { request } from './request';

// 登录
export const loginAPI = (account, password) => {
  return request('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ account, password }),
  });
};

// 注册
export const registerAPI = (formData) => {
  return request('/api/auth/register', {
    method: 'POST',
    body: formData,
  });
};