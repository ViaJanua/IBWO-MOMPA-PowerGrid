import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';   

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),   
    },
  },
  server: {
  port: 5173,
    proxy: {
      // api 开头的请求代理到 Flask 后端
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
      // 头像静态资源路径同上
      '/uploads': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
    },
  },
});