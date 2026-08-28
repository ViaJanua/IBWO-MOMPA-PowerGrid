<template>
  <div class="chart-panel">
    <div class="chart-title">{{ title }}</div>
    <div ref="chartRef" class="chart-container" :style="{ height: height + 'px' }"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick, onUnmounted } from 'vue';
import * as echarts from 'echarts';

const props = defineProps({
  title: { type: String, required: true },
  option: { type: Object, required: true },
  height: { type: Number, default: 300 }
});

const chartRef = ref(null);
let chartInstance = null;
let resizeObserver = null;

const initChart = () => {
  if (!chartRef.value) return;
  if (!chartInstance) {
    chartInstance = echarts.init(chartRef.value);
  }
  chartInstance.setOption(props.option, true);
  chartInstance.resize();
};

const setupResizeObserver = () => {
  if (!chartRef.value) return;
  if (window.ResizeObserver) {
    resizeObserver = new ResizeObserver(() => {
      if (chartInstance) {
        chartInstance.resize();
      }
    });
    resizeObserver.observe(chartRef.value);
  }
};

onMounted(() => {
  nextTick(() => {
    initChart();
    setupResizeObserver();
  });
});

watch(() => props.option, () => {
  nextTick(initChart);
}, { deep: true });

watch(() => props.height, () => {
  nextTick(() => {
    if (chartInstance) {
      chartInstance.resize();
    }
  });
});

onUnmounted(() => {
  if (resizeObserver) {
    resizeObserver.disconnect();
    resizeObserver = null;
  }
  if (chartInstance) {
    chartInstance.dispose();
    chartInstance = null;
  }
});
</script>

<style scoped>
.chart-panel {
  background: white;
  border-radius: 12px;
  border: 1px solid #eef2f7;
  padding: 12px;
}
.chart-title {
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
}
.chart-container {
  width: 100%;
}
</style>