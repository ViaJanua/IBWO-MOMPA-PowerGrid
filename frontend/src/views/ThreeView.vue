<template>
  <div class="three-page">
    <HeaderNav />

    <main class="page-content">
      <div class="container">
        <!-- 页面标题 -->
        <div class="page-header">
          <h1>三维数字孪生</h1>
          <p class="subtitle">配电网拓扑三维可视化，展示潮流分布与设备状态</p>
        </div>

        <!-- 3D场景 -->
        <div class="scene-wrapper">
          <ThreeScene ref="threeSceneRef" />
        </div>

        <!-- 控制按钮 -->
        <div class="controls-row">
          <button class="btn-control" @click="toggleRotate">
            {{ isAutoRotate ? '⏸️ 暂停旋转' : '▶️ 自动旋转' }}
          </button>
          <button class="btn-control" @click="resetView">🔄 重置视角</button>
          <span class="hint">鼠标 左键拖动 · 右键旋转 · 滚轮缩放</span>
        </div>

        <!-- 说明卡片 -->
        <div class="info-cards">
          <div class="info-card">
            <span class="info-icon">⚡</span>
            <div>
              <h4>节点电压</h4>
              <p>节点颜色表示当前电压水平（绿色正常，红色越限）</p>
            </div>
          </div>
          <div class="info-card">
            <span class="info-icon">🔵</span>
            <div>
              <h4>线路潮流</h4>
              <p>线路粗细与颜色深浅表示潮流大小和方向</p>
            </div>
          </div>
          <div class="info-card">
            <span class="info-icon">🟢</span>
            <div>
              <h4>设备状态</h4>
              <p>储能、OLTC、SVC 等设备以不同颜色高亮显示</p>
            </div>
          </div>
        </div>
      </div>
    </main>

    <FooterBar />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import HeaderNav from '@/components/HeaderNav.vue';
import FooterBar from '@/components/FooterBar.vue';
import ThreeScene from '@/components/ThreeScene.vue';

const threeSceneRef = ref(null);
const isAutoRotate = ref(false);

const toggleRotate = () => {
  if (threeSceneRef.value) {
    threeSceneRef.value.toggleAutoRotate();
    isAutoRotate.value = !isAutoRotate.value;
  }
};

const resetView = () => {
  if (threeSceneRef.value) {
    threeSceneRef.value.resetCamera();
  }
};
</script>

<style scoped>
.three-page {
  background: #f0f4f8;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.page-content {
  flex: 1;
  padding: 24px 0 48px;
}
.container {
  max-width: 1300px;
  margin: 0 auto;
  padding: 0 24px;
}
.page-header {
  margin-bottom: 24px;
}
.page-header h1 {
  font-size: 28px;
  font-weight: 700;
  color: #0a1628;
}
.page-header .subtitle {
  font-size: 15px;
  color: #6b7a8f;
}
.scene-wrapper {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  height: 550px;
}
.controls-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
  margin-top: 16px;
  padding: 12px 16px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.btn-control {
  padding: 8px 20px;
  border: none;
  border-radius: 8px;
  background: #2b6cb0;
  color: white;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-control:hover {
  background: #1a4f8b;
}
.hint {
  margin-left: auto;
  color: #6b7a8f;
  font-size: 13px;
}
.info-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-top: 20px;
}
.info-card {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px 20px;
  background: white;
  border-radius: 12px;
  border: 1px solid #eef2f7;
}
.info-icon {
  font-size: 28px;
  flex-shrink: 0;
}
.info-card h4 {
  font-size: 14px;
  font-weight: 600;
  color: #0a1628;
  margin: 0 0 4px 0;
}
.info-card p {
  font-size: 13px;
  color: #6b7a8f;
  margin: 0;
  line-height: 1.5;
}
@media (max-width: 768px) {
  .info-cards {
    grid-template-columns: 1fr;
  }
  .scene-wrapper {
    height: 350px;
  }
  .hint {
    display: none;
  }
}
</style>