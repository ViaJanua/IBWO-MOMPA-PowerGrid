<template>
  <header class="navbar">
    <div class="nav-container">
      <div class="logo">
        <span class="logo-icon"></span>
        <span class="logo-text">智能电网实时模拟平台</span>
      </div>
      <nav class="nav-links">
        <router-link to="/">首页</router-link>
        <router-link to="/tech-stack">技术栈</router-link>
        <router-link to="/data">电网模拟器</router-link>
        <router-link to="/algorithm">算法介绍</router-link>
        <router-link to="/three">三维展示</router-link>
        <a href="#" @click.prevent>关于平台</a>
      </nav>
      <div class="nav-right">
        <span class="status-badge">● 系统运行正常</span>
        <!-- 已登录：显示昵称 + 固定头像 -->
        <router-link v-if="auth.isLoggedIn && auth.user" to="/login" class="user-profile">
          <span class="user-nickname">{{ auth.user.nickname || auth.user.account }}</span>
          <span class="user-avatar">👤</span>
        </router-link>
        <!-- 未登录：显示 登录/注册 -->
        <router-link v-else to="/login" class="user-role">
          登录 / 注册
        </router-link>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useAuth } from '@/composables/useAuth';
const auth = useAuth();
</script>

<style scoped>
.navbar {
  background: #0a1628;
  color: white;
  padding: 0 24px;
  position: sticky;
  top: 0;
  z-index: 100;
}
.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}
.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 700;
}
.logo-text {
  color: white;
}
.nav-links {
  display: flex;
  gap: 32px;
}
.nav-links a {
  color: #a0aec0;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.2s;
}
.nav-links a:hover,
.nav-links a.router-link-active {
  color: white;
}
.nav-right {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 13px;
  color: #a0aec0;
}
.status-badge {
  color: #48bb78;
}
.user-profile {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  text-decoration: none;
  cursor: pointer;
}
.user-nickname {
  font-size: 14px;
  font-weight: 500;
  color: #e2e8f0;
}
.user-avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #2d3748;
  border: 2px solid #4a5568;
  font-size: 16px;
  color: #a0aec0;
}
.user-role {
  color: white;
  text-decoration: none;
  font-size: 14px;
}
@media (max-width: 768px) {
  .nav-links {
    gap: 16px;
  }
  .nav-links a {
    font-size: 13px;
  }
}
@media (max-width: 480px) {
  .nav-container {
    flex-wrap: wrap;
    height: auto;
    padding: 12px 0;
    gap: 8px;
  }
  .nav-links {
    flex-wrap: wrap;
    gap: 12px;
  }
}
</style>