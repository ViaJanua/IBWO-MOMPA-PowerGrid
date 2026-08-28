<template>
  <div class="page-wrapper">
    <HeaderNav />

    <main class="page-content">
      <!-- 首屏展示区 -->
      <section class="hero">
        <div class="container">
          <div class="hero-grid">
            <div class="hero-text">
              <h1>智能电网实时模拟平台</h1>
              <p class="hero-desc">
                面向新型电力系统的智能配电网调度与仿真平台
              </p>
              <p class="hero-sub">
                基于 IBWO-MOMPA 双算法协同优化，实现有功-无功联合调度，
                降低网损、提升电压、促进新能源消纳。
              </p>
              <div class="hero-buttons">
                <router-link to="/data" class="btn-primary">体验模拟器</router-link>
                <a href="#" class="btn-secondary" @click.prevent>观看演示</a>
              </div>
            </div>
            <div class="hero-stats">
              <div class="stat-card">
                <span class="stat-number">16</span>
                <span class="stat-label">四季 × 渗透率 场景</span>
              </div>
              <div class="stat-card">
                <span class="stat-number">94.28%</span>
                <span class="stat-label">最高网损降幅</span>
              </div>
              <div class="stat-card">
                <span class="stat-number">100%</span>
                <span class="stat-label">电压合格率</span>
              </div>
              <div class="stat-card">
                <span class="stat-number">4.43</span>
                <span class="stat-label">日购电成本（元）</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 核心功能模块 -->
      <section class="features">
        <div class="container">
          <h2 class="section-title">核心功能</h2>
          <div class="feature-grid">
            <div class="feature-card">
              <div class="feature-icon"></div>
              <h3>双算法协同优化</h3>
              <p>IBWO 经济调度 + MOMPA 无功优化，有功-无功联合调度</p>
            </div>
            <div class="feature-card">
              <div class="feature-icon"></div>
              <h3>多场景仿真</h3>
              <p>四季 × 四种渗透率，16组场景全覆盖验证</p>
            </div>
            <div class="feature-card">
              <div class="feature-icon"></div>
              <h3>实时数据可视化</h3>
              <p>功率平衡、网损对比、电压监控、储能SOC动态展示</p>
            </div>
            <div class="feature-card">
              <div class="feature-icon"></div>
              <h3>逐时调节方案</h3>
              <p>储能、OLTC、SVC、电容器、需求响应完整指令输出</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 技术栈简介 -->
      <section class="tech-intro">
        <div class="container">
          <div class="tech-box">
            <span class="tech-badge">技术栈</span>
            <span>Vue 3 · ECharts · Flask · PostgreSQL · Three.js</span>
            <router-link to="/tech-stack" class="tech-link">查看详情 →</router-link>
          </div>
        </div>
      </section>
    </main>

    <FooterBar />
  </div>
</template>

<script setup>
import HeaderNav from '@/components/HeaderNav.vue';
import FooterBar from '@/components/FooterBar.vue';
</script>

<style scoped>
/* 首屏展示区 */
.hero {
  background: linear-gradient(135deg, #0a1628 0%, #1a365d 100%);
  padding: 64px 0 48px;
  color: white;
}
.hero-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  align-items: center;
}
.hero-text h1 {
  font-size: 38px;
  font-weight: 700;
  margin-bottom: 12px;
}
.hero-desc {
  font-size: 18px;
  color: #bee3f8;
  margin-bottom: 8px;
}
.hero-sub {
  font-size: 15px;
  color: #a0aec0;
  line-height: 1.8;
  margin-bottom: 24px;
}
.hero-buttons {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}
.btn-secondary {
  display: inline-block;
  padding: 10px 28px;
  border: 1px solid rgba(255,255,255,0.3);
  border-radius: 8px;
  color: white;
  font-size: 15px;
  transition: background 0.2s;
}
.btn-secondary:hover {
  background: rgba(255,255,255,0.1);
}
.hero-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.stat-card {
  background: rgba(255,255,255,0.08);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  backdrop-filter: blur(4px);
}
.stat-number {
  display: block;
  font-size: 32px;
  font-weight: 700;
  color: #63b3ed;
}
.stat-label {
  font-size: 13px;
  color: #a0aec0;
}

/* 核心功能 */
.features {
  padding: 48px 0;
  background: white;
}
.section-title {
  font-size: 28px;
  font-weight: 700;
  color: #0a1628;
  text-align: center;
  margin-bottom: 32px;
}
.feature-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}
.feature-card {
  background: #f8fafc;
  border-radius: 12px;
  padding: 24px;
  text-align: center;
  border: 1px solid #eef2f7;
  transition: transform 0.2s;
}
.feature-card:hover {
  transform: translateY(-4px);
}
.feature-icon {
  font-size: 36px;
  margin-bottom: 12px;
}
.feature-card h3 {
  font-size: 16px;
  font-weight: 600;
  color: #0a1628;
  margin-bottom: 8px;
}
.feature-card p {
  font-size: 14px;
  color: #6b7a8f;
  line-height: 1.6;
}

/* 技术栈简介 */
.tech-intro {
  padding: 32px 0;
  background: #f0f4f8;
}
.tech-box {
  background: white;
  border-radius: 12px;
  padding: 16px 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
  border: 1px solid #eef2f7;
}
.tech-badge {
  background: #2b6cb0;
  color: white;
  padding: 2px 12px;
  border-radius: 12px;
  font-size: 12px;
}
.tech-box span {
  font-size: 14px;
  color: #4a5568;
}
.tech-link {
  margin-left: auto;
  color: #2b6cb0;
  font-weight: 500;
  font-size: 14px;
}

/* 响应式 */
@media (max-width: 1024px) {
  .hero-grid {
    grid-template-columns: 1fr;
    gap: 32px;
  }
  .feature-grid {
    grid-template-columns: 1fr 1fr;
  }
}
@media (max-width: 768px) {
  .hero-text h1 {
    font-size: 28px;
  }
  .hero-stats {
    grid-template-columns: 1fr 1fr;
  }
  .feature-grid {
    grid-template-columns: 1fr;
  }
  .tech-box {
    flex-direction: column;
    align-items: flex-start;
  }
  .tech-link {
    margin-left: 0;
  }
}
</style>