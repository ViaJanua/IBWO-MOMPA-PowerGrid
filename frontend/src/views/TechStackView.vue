<template>
  <div class="algorithm-page">
    <!-- 公共导航栏 -->
    <HeaderNav />

    <div class="breadcrumb-bar">
      <div class="container">
        <span>首页 / <strong>技术栈</strong></span>
      </div>
    </div>

    <section class="page-header">
      <div class="container">
        <h1>技术栈</h1>
        <p class="subtitle">
          智能电网实时模拟平台采用现代化的技术栈构建，前后端分离，微服务架构，高性能计算与实时通信相结合，
          为大规模电网实时仿真提供稳定、可靠、可扩展的技术支撑。
        </p>
      </div>
    </section>

    <section class="tech-grid">
      <div class="container">
        <div class="grid-cards">
          <div class="tech-card">
            <div class="card-icon"></div>
            <h3>Vue 3</h3>
            <p class="tech-label">前端框架</p>
            <p class="tech-desc">基于Vue 3的组合式 API，配合Vite构建工具，提供优秀的开发体验和性能优化。</p>
          </div>
          <div class="tech-card">
            <div class="card-icon"></div>
            <h3>ECharts</h3>
            <p class="tech-label">图表可视化</p>
            <p class="tech-desc">基于ECharts 5构建动态电网数据图表，支持功率平衡、网损对比、电压监控等多种可视化需求。</p>
          </div>
          <div class="tech-card">
            <div class="card-icon"></div>
            <h3>TypeScript</h3>
            <p class="tech-label">语言</p>
            <p class="tech-desc">JavaScript的超集，提供静态类型检查，增强代码可维护性和可读性，提升大型项目开发效率。</p>
          </div>
          <div class="tech-card">
            <div class="card-icon"></div>
            <h3>Flask</h3>
            <p class="tech-label">后端框架</p>
            <p class="tech-desc">轻量级Python Web框架，提供RESTful API服务，与前端高效交互，支撑算法服务的快速部署。</p>
          </div>
          <div class="tech-card">
            <div class="card-icon"></div>
            <h3>PostgreSQL</h3>
            <p class="tech-label">数据库</p>
            <p class="tech-desc">强大的开源关系型数据库，支持复杂查询、高并发和数据完整性，存储仿真场景与历史数据。</p>
          </div>
          <div class="tech-card">
            <div class="card-icon"></div>
            <h3>WebSocket</h3>
            <p class="tech-label">实时通信</p>
            <p class="tech-desc">基于WebSocket协议实现双向通信，低延迟推送仿真数据和系统状态，支持实时监控与交互。</p>
          </div>
          <div class="tech-card">
            <div class="card-icon"></div>
            <h3>Three.js</h3>
            <p class="tech-label">3D渲染</p>
            <p class="tech-desc">基于WebGL的3D图形库，构建电网拓扑、设备模型和三维可视化场景，使用Blender进行模型渲染，提供沉浸式交互体验。</p>
          </div>
          <div class="tech-card">
            <div class="card-icon"></div>
            <h3>Python 算法服务</h3>
            <p class="tech-label">算法引擎</p>
            <p class="tech-desc">基于Python的算法服务，提供潮流计算、优化调度、故障分析等电力系统核心算法能力，支持高性能计算。</p>
          </div>
        </div>
      </div>
    </section>

    <section class="architecture">
      <div class="container">
        <div class="arch-box">
          <p>
            平台采用微服务架构，各服务模块化设计，支持Docker容器化部署，Kubernetes编排，
            具备良好的可扩展性和高可用性。
          </p>
        </div>
      </div>
    </section>

    <footer class="footer">
      <div class="container">
        <p>© 2026 智能电网实时模拟平台 · 基于 IBWO-MOMPA 双算法协同优化</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import HeaderNav from '@/components/HeaderNav.vue';
import { useAuth } from '@/composables/useAuth';
const auth = useAuth();
</script>

<style scoped>
.tech-stack-page {
  background: #f0f4f8;
  min-height: 100vh;
}
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
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
.nav-links a.active {
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
.breadcrumb-bar {
  background: white;
  padding: 12px 0;
  border-bottom: 1px solid #eef2f7;
  font-size: 14px;
  color: #6b7a8f;
}
.breadcrumb-bar strong {
  color: #2c3e50;
}
.page-header {
  padding: 48px 0 32px;
  background: white;
  border-bottom: 1px solid #eef2f7;
}
.page-header h1 {
  font-size: 32px;
  font-weight: 700;
  color: #0a1628;
  margin-bottom: 12px;
}
.page-header .subtitle {
  font-size: 16px;
  color: #6b7a8f;
  line-height: 1.8;
  max-width: 800px;
}
.tech-grid {
  padding: 48px 0;
}
.grid-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}
.tech-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  border: 1px solid #eef2f7;
  transition: transform 0.2s, box-shadow 0.2s;
}
.tech-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
}
.tech-card .card-icon {
  font-size: 32px;
  margin-bottom: 12px;
}
.tech-card h3 {
  font-size: 16px;
  font-weight: 600;
  color: #0a1628;
  margin-bottom: 4px;
}
.tech-card .tech-label {
  font-size: 12px;
  color: #6b7a8f;
  margin-bottom: 12px;
}
.tech-card .tech-desc {
  font-size: 14px;
  color: #4a5568;
  line-height: 1.6;
}
.architecture {
  padding: 0 0 48px;
}
.arch-box {
  background: #edf2f7;
  border-radius: 12px;
  padding: 20px 24px;
  border-left: 4px solid #2b6cb0;
}
.arch-box p {
  font-size: 14px;
  color: #2c3e50;
  line-height: 1.8;
  margin: 0;
}
.footer {
  background: #0a1628;
  padding: 20px 0;
  text-align: center;
}
.footer p {
  color: #6b7a8f;
  font-size: 13px;
  margin: 0;
}
@media (max-width: 1024px) {
  .grid-cards { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 768px) {
  .grid-cards { grid-template-columns: 1fr 1fr; }
  .nav-links { gap: 16px; }
  .nav-links a { font-size: 13px; }
  .page-header h1 { font-size: 24px; }
}
@media (max-width: 480px) {
  .grid-cards { grid-template-columns: 1fr; }
  .nav-container { flex-wrap: wrap; height: auto; padding: 12px 0; gap: 8px; }
  .nav-links { flex-wrap: wrap; gap: 12px; }
}
</style>