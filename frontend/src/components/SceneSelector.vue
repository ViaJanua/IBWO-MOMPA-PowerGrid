<template>
  <div class="scene-selector">
    <div class="selector-group">
      <label>季节</label>
      <select v-model="season">
        <option value="spring">春季</option>
        <option value="summer">夏季</option>
        <option value="autumn">秋季</option>
        <option value="winter">冬季</option>
      </select>
    </div>
    <div class="selector-group">
      <label>渗透率</label>
      <select v-model="penetration">
        <option value="0%">0%</option>
        <option value="5%">5%</option>
        <option value="10%">10%</option>
        <option value="15%">15%</option>
      </select>
    </div>
    <button class="btn-primary" @click="loadData">更新数据</button>
    <span v-if="loading" class="status-text"> 加载中...</span>
    <span v-else-if="loaded" class="status-text success">✅ {{ sceneName }} 已加载</span>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const emit = defineEmits(['update']);

const season = ref('autumn');
const penetration = ref('15%');
const loading = ref(false);
const loaded = ref(false);

const sceneName = computed(() => `${season.value}_${penetration.value}`);

const loadData = () => {
  loading.value = true;
  loaded.value = false;
  emit('update', { season: season.value, penetration: penetration.value });
  // 父组件加载完成发来提示
};

// 外部可设置 loading 状态
defineExpose({ setLoading: (val) => { loading.value = val; if (!val) loaded.value = true; } });

// 监听变化自动加载
watch([season, penetration], () => {
  // 不自动加载，等待用户点击
});
</script>

<style scoped>
.scene-selector {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
  background: white;
  padding: 16px 20px;
  border-radius: 12px;
  border: 1px solid #eef2f7;
  margin-bottom: 20px;
}
.selector-group {
  display: flex;
  align-items: center;
  gap: 8px;
}
.selector-group label {
  font-size: 14px;
  font-weight: 500;
  color: #2c3e50;
}
.selector-group select {
  padding: 6px 12px;
  border-radius: 6px;
  border: 1px solid #d0d7de;
  font-size: 14px;
  background: white;
  outline: none;
}
.selector-group select:focus {
  border-color: #2b6cb0;
}
.status-text {
  font-size: 13px;
  color: #6b7a8f;
  margin-left: 8px;
}
.status-text.success {
  color: #38a169;
}
@media (max-width: 600px) {
  .scene-selector {
    flex-direction: column;
    align-items: stretch;
  }
  .selector-group {
    justify-content: space-between;
  }
}
</style>