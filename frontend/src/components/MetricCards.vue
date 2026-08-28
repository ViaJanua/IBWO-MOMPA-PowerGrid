<template>
  <div class="metric-cards">
    <div class="card" v-for="item in cards" :key="item.key">
      <div class="card-label">{{ item.label }}</div>
      <div class="card-value">{{ item.value }}</div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  summary: {
    type: Object,
    required: true
  }
});

// 格式化数值：将 NaN/null/undefined 转为 "0"
const formatValue = (value) => {
  if (value === null || value === undefined || value === '') return '0';
  const num = Number(value);
  if (isNaN(num)) return '0';
  // 数字保留两位小数
  return num.toFixed(2);
};

const cards = computed(() => [
  { key: 'cost', label: ' 日总购电成本', value: formatValue(props.summary['日总购电成本']) },
  { key: 'loss', label: ' 网损降低率', value: formatValue(props.summary['网损降低率']) },
  { key: 'voltage', label: ' 电压合格率', value: formatValue(props.summary['电压合格率']) },
  { key: 'peak', label: ' 峰谷差削减率', value: formatValue(props.summary['峰谷差削减率']) },
]);
</script>

<style scoped>
.metric-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}
.card {
  background: white;
  padding: 16px 20px;
  border-radius: 12px;
  border-left: 4px solid #2b6cb0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.card-label {
  font-size: 13px;
  color: #6b7a8f;
  margin-bottom: 4px;
}
.card-value {
  font-size: 28px;
  font-weight: 700;
  color: #0a1628;
}
@media (max-width: 768px) {
  .metric-cards {
    grid-template-columns: 1fr 1fr;
  }
}
@media (max-width: 480px) {
  .metric-cards {
    grid-template-columns: 1fr;
  }
}
</style>