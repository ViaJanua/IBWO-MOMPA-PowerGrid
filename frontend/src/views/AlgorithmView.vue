<template>
  <div class="algorithm-page">
    <!-- 公共导航栏 -->
    <HeaderNav />

    <!-- 位置导航 -->
    <div class="breadcrumb-bar">
      <div class="container">
        <span>首页 / <strong>算法介绍</strong></span>
      </div>
    </div>

    <!-- 页面标题  -->
    <section class="page-header">
      <div class="container">
        <h1>IBWO-MOMPA 双算法协同优化</h1>
        <p class="subtitle">
          基于改进黑寡妇优化算法（IBWO）与改进多目标海洋捕食者算法（MOMPA）的有功-无功协同调度，
          实现配电网经济性与电能质量的联合优化。
        </p>
      </div>
    </section>

    <!-- 算法架构 -->
    <section class="arch-section">
      <div class="container">
        <div class="arch-grid">
          <div class="arch-card">
            <div class="arch-header">
              <span class="arch-icon"></span>
              <div>
                <h3>IBWO 经济调度</h3>
                <span class="arch-tag">有功层</span>
              </div>
            </div>
            <p class="arch-desc">
              以最小化用户总电费与全天负载波动为综合优化目标，输出各时段储能充放电计划与购电计划。
            </p>
            <div class="improve-list">
              <div class="improve-item">
                <span class="badge">改进1</span>
                <span>共享适应度机制 — 延缓早熟收敛</span>
              </div>
              <div class="improve-item">
                <span class="badge">改进2</span>
                <span>相似感知自适应交配 — 动态平衡探索与开发</span>
              </div>
              <div class="improve-item">
                <span class="badge">改进3</span>
                <span>高斯-柯西双模扰动变异 — 全局+局部搜索</span>
              </div>
              <div class="improve-item">
                <span class="badge">改进4</span>
                <span>吸引法边界修正 — 保持解空间连续性</span>
              </div>
            </div>
            <div class="arch-footer">
              <span class="dim-label">决策变量</span>
              <span class="dim-value">48维（储能24 + DR 24）</span>
            </div>
          </div>

          <div class="arch-card">
            <div class="arch-header">
              <span class="arch-icon"></span>
              <div>
                <h3>MOMPA 无功优化</h3>
                <span class="arch-tag">无功层</span>
              </div>
            </div>
            <p class="arch-desc">
              以系统有功损耗最小与节点电压偏差最小为双目标，优化OLTC档位、SVC出力与电容器投切策略。
            </p>
            <div class="improve-list">
              <div class="improve-item">
                <span class="badge">改进1</span>
                <span>Tent混沌映射 + 动态反向学习 — 提升初始种群质量</span>
              </div>
              <div class="improve-item">
                <span class="badge">改进2</span>
                <span>精英-最稀疏区域引导 — 提升Pareto前沿均匀性</span>
              </div>
              <div class="improve-item">
                <span class="badge">改进3</span>
                <span>Sigmoid非线性收敛因子 — 探索与开发平滑过渡</span>
              </div>
              <div class="improve-item">
                <span class="badge">改进4</span>
                <span>差异化差分算子 — 支配/非支配个体分别引导</span>
              </div>
            </div>
            <div class="arch-footer">
              <span class="dim-label">决策变量</span>
              <span class="dim-value">5维（OLTC + SVC + 3组电容器）</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 闭环迭代流程 -->
    <section class="flow-section">
      <div class="container">
        <h2 class="section-title">双模型闭环迭代机制</h2>
        <div class="flow-diagram">
          <div class="flow-step">
            <div class="step-number">1</div>
            <div class="step-content">
              <h4>IBWO 经济调度</h4>
              <p>输出储能充放电计划 + 需求响应比例</p>
            </div>
          </div>
          <div class="flow-arrow">→</div>
          <div class="flow-step">
            <div class="step-number">2</div>
            <div class="step-content">
              <h4>MOMPA 无功优化</h4>
              <p>输出 OLTC档位 + SVC + 电容器投切方案</p>
            </div>
          </div>
          <div class="flow-arrow">→</div>
          <div class="flow-step">
            <div class="step-number">3</div>
            <div class="step-content">
              <h4>潮流计算与反馈</h4>
              <p>计算全网损耗 + 节点电压，反馈修正</p>
            </div>
          </div>
          <div class="flow-arrow">⟳</div>
          <div class="flow-step">
            <div class="step-number">✓</div>
            <div class="step-content">
              <h4>收敛输出</h4>
              <p>全局最优联合调度方案</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 16组场景结果 -->
    <section class="result-section">
      <div class="container">
        <h2 class="section-title">16组场景全覆盖检验</h2>
        <p class="section-sub">
          覆盖四季（春/夏/秋/冬）× 四种渗透率（0%/5%/10%/15%）场景，算法均取得显著优化效果。
        </p>
        <div class="result-tables">
          <div class="table-wrapper">
            <h4>电压合格率（优化后）</h4>
            <table class="result-table">
              <thead>
                <tr><th>季节</th><th>0%</th><th>5%</th><th>10%</th><th>15%</th></tr>
              </thead>
              <tbody>
                <tr><td>春季</td><td>100%</td><td>100%</td><td>100%</td><td>100%</td></tr>
                <tr><td>夏季</td><td>100%</td><td>100%</td><td>100%</td><td>95.83%</td></tr>
                <tr><td>秋季</td><td>100%</td><td>100%</td><td>100%</td><td>91.67%</td></tr>
                <tr><td>冬季</td><td>100%</td><td>91.67%</td><td>91.67%</td><td>62.50%</td></tr>
              </tbody>
            </table>
          </div>
          <div class="table-wrapper">
            <h4>网损降低率</h4>
            <table class="result-table">
              <thead>
                <tr><th>季节</th><th>0%</th><th>5%</th><th>10%</th><th>15%</th></tr>
              </thead>
              <tbody>
                <tr><td>春季</td><td>—</td><td>—</td><td>-2.56%</td><td><strong>94.28%</strong></td></tr>
                <tr><td>夏季</td><td><strong>93.68%</strong></td><td>81.38%</td><td>63.20%</td><td>41.11%</td></tr>
                <tr><td>秋季</td><td><strong>91.69%</strong></td><td><strong>71.77%</strong></td><td>45.98%</td><td>22.35%</td></tr>
                <tr><td>冬季</td><td>31.99%</td><td>18.56%</td><td>18.40%</td><td>14.64%</td></tr>
              </tbody>
            </table>
            <p class="table-note">春季 0%和5% 因新能源完全覆盖负荷，基准网损为0，降损率不适用。</p>
          </div>
        </div>
        <div class="highlight-box">
          <span class="highlight-icon"></span>
          <div>
            <strong>最佳结果：</strong>
            春季15%场景 — 网损降幅 <strong>94.28%</strong>，电压合格率 <strong>100%</strong>
          </div>
        </div>
      </div>
    </section>

    <!-- 底部页脚 -->
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
.algorithm-page {
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
.arch-section {
  padding: 48px 0;
}
.arch-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}
.arch-card {
  background: white;
  border-radius: 12px;
  padding: 28px;
  border: 1px solid #eef2f7;
}
.arch-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}
.arch-icon {
  font-size: 28px;
}
.arch-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #0a1628;
  margin: 0;
}
.arch-tag {
  font-size: 11px;
  background: #edf2f7;
  padding: 2px 10px;
  border-radius: 10px;
  color: #4a5568;
}
.arch-desc {
  font-size: 14px;
  color: #4a5568;
  line-height: 1.6;
  margin-bottom: 16px;
}
.improve-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 16px;
}
.improve-item {
  font-size: 13px;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 8px;
}
.improve-item .badge {
  font-size: 10px;
  background: #2b6cb0;
  color: white;
  padding: 1px 8px;
  border-radius: 8px;
  flex-shrink: 0;
}
.arch-footer {
  border-top: 1px solid #eef2f7;
  padding-top: 12px;
  display: flex;
  justify-content: space-between;
  font-size: 13px;
}
.dim-label {
  color: #6b7a8f;
}
.dim-value {
  font-weight: 600;
  color: #0a1628;
}
.flow-section {
  padding: 48px 0;
  background: white;
}
.section-title {
  font-size: 24px;
  font-weight: 700;
  color: #0a1628;
  margin-bottom: 24px;
}
.flow-diagram {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  background: #f8fafc;
  border-radius: 12px;
  padding: 24px 32px;
  border: 1px solid #eef2f7;
}
.flow-step {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  min-width: 140px;
}
.step-number {
  width: 36px;
  height: 36px;
  background: #2b6cb0;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
}
.flow-step .step-content h4 {
  font-size: 14px;
  font-weight: 600;
  color: #0a1628;
  margin: 0;
}
.flow-step .step-content p {
  font-size: 12px;
  color: #6b7a8f;
  margin: 0;
}
.flow-arrow {
  font-size: 20px;
  color: #2b6cb0;
  flex-shrink: 0;
  padding: 0 4px;
}
.result-section {
  padding: 48px 0;
}
.section-sub {
  font-size: 15px;
  color: #6b7a8f;
  margin-bottom: 32px;
}
.result-tables {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}
.table-wrapper h4 {
  font-size: 15px;
  font-weight: 600;
  color: #0a1628;
  margin-bottom: 12px;
}
.result-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #eef2f7;
}
.result-table th {
  background: #f8fafc;
  padding: 10px 12px;
  text-align: center;
  border-bottom: 2px solid #e2e8f0;
  font-weight: 600;
}
.result-table td {
  padding: 8px 12px;
  text-align: center;
  border-bottom: 1px solid #f0f4f8;
}
.result-table td strong {
  color: #2b6cb0;
}
.table-note {
  font-size: 12px;
  color: #a0aec0;
  margin-top: 8px;
}
.highlight-box {
  margin-top: 32px;
  background: #ebf8ff;
  border-radius: 12px;
  padding: 16px 24px;
  border: 1px solid #bee3f8;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 15px;
  color: #2c3e50;
}
.highlight-icon {
  font-size: 28px;
}
.highlight-box strong {
  color: #2b6cb0;
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
  .arch-grid { grid-template-columns: 1fr; }
  .result-tables { grid-template-columns: 1fr; }
  .flow-diagram { flex-direction: column; align-items: stretch; }
  .flow-arrow { transform: rotate(90deg); padding: 4px 0; text-align: center; }
  .flow-step { min-width: unset; }
}
@media (max-width: 768px) {
  .nav-links { gap: 16px; }
  .nav-links a { font-size: 13px; }
  .page-header h1 { font-size: 24px; }
  .flow-diagram { padding: 16px; }
}
@media (max-width: 480px) {
  .nav-container { flex-wrap: wrap; height: auto; padding: 12px 0; gap: 8px; }
  .nav-links { flex-wrap: wrap; gap: 12px; }
  .arch-card { padding: 16px; }
  .improve-item { font-size: 12px; }
  .result-table { font-size: 12px; }
  .result-table th, .result-table td { padding: 6px 8px; }
}
</style>