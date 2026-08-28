<template>
  <div class="page-wrapper">
    <HeaderNav />

    <main class="page-content">
      <div class="container">
        <!--  页面标题  -->
        <div class="page-header">
          <h1>电网模拟器</h1>
          <p class="subtitle">选择季节与渗透率，查看 IBWO-MOMPA 双算法协同调度结果</p>
        </div>

<!--  控制行：场景选择器 + 模式选项  -->
<div class="control-row">
  <SceneSelector @update="onSceneUpdate" />

  <div class="mode-options">
    <label class="mode-option">
      <input type="checkbox" :checked="selectedMode === 'fast'" @change="toggleMode('fast')" />
      <span class="checkmark"></span>
      极速
    </label>
    <label class="mode-option">
      <input type="checkbox" :checked="selectedMode === 'accurate'" @change="toggleMode('accurate')" />
      <span class="checkmark"></span>
      精确
    </label>
    <button class="cancel-btn" @click="cancelMode">取消</button>
    <span class="mode-hint" v-if="selectedMode === null">请选择运行模式</span>
    <span class="mode-hint" v-else-if="selectedMode === 'fast'">读取数据</span>
    <span class="mode-hint" v-else>运行算法</span>
  </div>
</div>

        <!--  加载状态  -->
        <div v-if="loading" class="loading-state"> 加载中...</div>

        <!-- 数据展示  -->
        <template v-else-if="data">
          <!-- 指标卡片 -->
          <MetricCards :summary="data.summary" />

          <!-- 图表面板 -->
          <div class="charts-grid">
            <EChartsPanel
              v-for="chart in chartConfigs"
              :key="chart.id"
              :title="chart.title"
              :option="chart.option"
              :height="300"
            />
          </div>

          <!--  调节方案  -->
          <div class="scheme-section">
            <h3>逐时调节方案</h3>

            <div class="text-description">
              <h4> </h4>
              <div class="desc-grid">
                <div 
                  v-for="(item, idx) in scheduleText" 
                  :key="idx"
                  class="desc-item"
                  :class="{
                    'charge': item.action === '充电',
                    'discharge': item.action === '放电',
                    'idle': item.action === '待机'
                  }"
                >
                  <span class="desc-time">{{ item.time }}</span>
                  <span class="desc-action">{{ item.action }}</span>
                  <span class="desc-detail">{{ item.detail }}</span>
                </div>
              </div>

              <div class="schedule-summary">
                <div class="summary-item">
                  <span class="summary-label"> 总充电量</span>
                  <span class="summary-value">{{ totalCharge.toFixed(2) }} MWh</span>
                </div>
                <div class="summary-item">
                  <span class="summary-label"> 总放电量</span>
                  <span class="summary-value">{{ totalDischarge.toFixed(2) }} MWh</span>
                </div>
                <div class="summary-item">
                  <span class="summary-label"> 购电费用</span>
                  <span class="summary-value">{{ summaryData?.['日总购电成本'] || '--' }} 元</span>
                </div>
                <div class="summary-item">
                  <span class="summary-label"> 碳减排量</span>
                  <span class="summary-value">{{ carbonReduction.toFixed(2) }} kg</span>
                </div>
                <div class="summary-item">
                  <span class="summary-label"> 平均SOC</span>
                  <span class="summary-value">{{ avgSOC.toFixed(1) }}%</span>
                </div>
              </div>
            </div>

            <RegulationTable :data="data.hourly" />
          </div>
        </template>

        <div v-else class="empty-state">
          <p>暂无数据，请选择场景后点击加载</p>
        </div>
      </div>
    </main>

    <FooterBar />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import HeaderNav from '@/components/HeaderNav.vue';
import FooterBar from '@/components/FooterBar.vue';
import SceneSelector from '@/components/SceneSelector.vue';
import MetricCards from '@/components/MetricCards.vue';
import EChartsPanel from '@/components/EChartsPanel.vue';
import RegulationTable from '@/components/RegulationTable.vue';

const loading = ref(false);
const data = ref(null);

//  演示模式：true=极速，false=精确 
const selectedMode = ref(null);

const toggleMode = (mode) => {
  if (selectedMode.value === mode) {
    selectedMode.value = null;  
  } else {
    selectedMode.value = mode;  
  }
};

// 取消按钮：清除选中的模式
const cancelMode = () => {
  selectedMode.value = null;
};

// 文字描述 
const scheduleText = computed(() => {
  if (!data.value) return [];
  const hourly = data.value.hourly;

  return hourly.map(d => {
    const time = d['时段'] || '';
    const storagePower = Number(d['储能功率(MW)']) || 0;
    const soc = Number(d['储能SOC']) || 0;
    const oltc = Number(d['OLTC分接头档位']) || 0;
    const cap17 = Number(d['17号电容器投切档位']) || 0;
    const cap29 = Number(d['29号电容器投切档位']) || 0;
    const cap32 = Number(d['32号电容器投切档位']) || 0;
    const svc = Number(d['SVC无功容量(Mvar)']) || 0;
    const dr = Number(d['需求响应比例']) || 0;

    let action = '待机';
    if (storagePower > 0.01) action = '放电';
    else if (storagePower < -0.01) action = '充电';

    const caps = [];
    if (cap17 > 0) caps.push(`17号电容 ${cap17} kVar`);
    if (cap29 > 0) caps.push(`29号电容 ${cap29} kVar`);
    if (cap32 > 0) caps.push(`32号电容 ${cap32} kVar`);
    const capText = caps.length > 0 ? `，投入 ${caps.join('、')}` : '，未投入电容器';

    const svcText = svc !== 0 ? `，SVC出力 ${svc.toFixed(2)} Mvar` : '';
    const drText = dr !== 0 ? `，需求响应 ${(dr * 100).toFixed(1)}%` : '，无需需求响应';

    const detail = `储能SOC ${(soc * 100).toFixed(1)}%，OLTC ${oltc} 档${capText}${svcText}${drText}`;

    return { time, action, detail };
  });
});

//  调度计划概要统计 
const summaryData = computed(() => data.value?.summary || null);
const hourlyData = computed(() => data.value?.hourly || []);

const totalCharge = computed(() => {
  return hourlyData.value.reduce((sum, d) => {
    const p = Number(d['储能功率(MW)']) || 0;
    return p < 0 ? sum + Math.abs(p) : sum;
  }, 0);
});

const totalDischarge = computed(() => {
  return hourlyData.value.reduce((sum, d) => {
    const p = Number(d['储能功率(MW)']) || 0;
    return p > 0 ? sum + p : sum;
  }, 0);
});

const avgSOC = computed(() => {
  const list = hourlyData.value.map(d => Number(d['储能SOC']) || 0);
  if (list.length === 0) return 0;
  return (list.reduce((a, b) => a + b, 0) / list.length) * 100;
});

const carbonReduction = computed(() => {
  const totalRenewable = hourlyData.value.reduce((sum, d) => {
    return sum + (Number(d['新能源出力(MW)']) || 0);
  }, 0);
  return totalRenewable * 0.5;
});

//  图表配置 
const chartConfigs = computed(() => {
  if (!data.value) return [];
  const h = data.value.hourly;
  const hours = h.map(d => d['时段']);

  return [
    {
      id: 'power',
      title: '功率平衡图',
      option: {
        tooltip: { trigger: 'axis' },
        legend: { data: ['负荷功率', '新能源出力', '电网购电'], bottom: 0 },
        grid: { left: 40, right: 40, top: 40, bottom: 50 },
        xAxis: { type: 'category', data: hours, name: '时段/h', nameLocation: 'end' },
        yAxis: { type: 'value', name: '功率 (MW)', nameLocation: 'end' },
        series: [
          { name: '负荷功率', type: 'line', data: h.map(d => d['负荷功率(MW)']), smooth: true, lineStyle: { color: '#2b6cb0', width: 2 } },
          { name: '新能源出力', type: 'line', data: h.map(d => d['新能源出力(MW)']), smooth: true, lineStyle: { color: '#38a169', width: 2 } },
          { name: '电网购电', type: 'line', data: h.map(d => d['电网购电(MW)']), smooth: true, lineStyle: { color: '#dd6b20', width: 2 } }
        ],
        animationDuration: 1500,
        animationEasing: 'cubicOut'
      }
    },
    {
      id: 'loss',
      title: '网损对比',
      option: {
        tooltip: { trigger: 'axis' },
        legend: { data: ['基础方案', 'MOMPA优化后'], bottom: 0 },
        grid: { left: 40, right: 40, top: 40, bottom: 50 },
        xAxis: { type: 'category', data: hours, name: '时段/h', nameLocation: 'end' },
        yAxis: { type: 'value', name: '网损 (MW)', nameLocation: 'end' },
        series: [
          { name: '基础方案', type: 'bar', data: h.map(d => d['基础方案网损(MW)']), barWidth: '30%', itemStyle: { color: '#bdc3c7', opacity: 0.7 } },
          { name: 'MOMPA优化后', type: 'bar', data: h.map(d => d['实时网损(MW)']), barWidth: '30%', itemStyle: { color: '#3498db', borderRadius: [2, 2, 0, 0] } }
        ],
        animationDuration: 1500,
        animationEasing: 'cubicOut'
      }
    },
    {
      id: 'voltage',
      title: '节点最低电压对比',
      option: {
        tooltip: { trigger: 'axis' },
        legend: { data: ['基础方案', '协同优化后', '电压下限0.95pu'], bottom: 0 },
        grid: { left: 40, right: 60, top: 40, bottom: 50 },
        xAxis: { type: 'category', data: hours, name: '时段/h', nameLocation: 'end' },
        yAxis: { type: 'value', name: '电压 (pu)', min: 0.85, max: 1.05, nameLocation: 'end' },
        series: [
          { name: '基础方案', type: 'line', data: h.map(d => d['基础方案最低电压']), smooth: true, lineStyle: { color: '#e53e3e', width: 2, type: 'dashed' } },
          { name: '协同优化后', type: 'line', data: h.map(d => d['节点最低电压(p.u.)']), smooth: true, lineStyle: { color: '#2b6cb0', width: 2 }, areaStyle: { color: 'rgba(43,108,176,0.1)' } },
          { name: '电压下限0.95pu', type: 'line', data: Array(24).fill(0.95), lineStyle: { color: '#e53e3e', width: 1, type: 'dotted' }, symbol: 'none' }
        ],
        animationDuration: 1500,
        animationEasing: 'cubicOut'
      }
    },
    {
      id: 'storage',
      title: '储能充放电与SOC',
      option: {
        tooltip: { trigger: 'axis' },
        legend: { data: ['储能功率（正值放电）', 'SOC'], bottom: 0 },
        grid: { left: 40, right: 40, top: 40, bottom: 50 },
        xAxis: { type: 'category', data: hours, name: '时段/h', nameLocation: 'end' },
        yAxis: [
          { type: 'value', name: '功率 (MW)', min: -0.8, max: 0.8, nameLocation: 'end' },
          { type: 'value', name: 'SOC (p.u.)', min: 0, max: 1, nameLocation: 'end' }
        ],
        series: [
          { name: '储能功率（正值放电）', type: 'bar', data: h.map(d => d['储能功率(MW)']), itemStyle: { color: (p) => p.value >= 0 ? '#38a169' : '#e53e3e' } },
          { name: 'SOC', type: 'line', yAxisIndex: 1, data: h.map(d => d['储能SOC']), smooth: true, lineStyle: { color: '#805ad5', width: 2 } }
        ],
        animationDuration: 1500,
        animationEasing: 'cubicOut'
      }
    }
  ];
});

// 更新数据 
const onSceneUpdate = (payload) => {
  // 如果未选择模式，自动默认为极速
  if (selectedMode.value === null) {
    selectedMode.value = 'fast';
  }
  
  loading.value = true;
  
  if (selectedMode.value === 'fast') {
    // 极速模式：读取预计算 CSV
    fetch(`/api/data?season=${payload.season}&penetration=${payload.penetration}`)
      .then(res => res.json())
      .then(d => {
        if (d.error) throw new Error(d.error);
        data.value = d;
      })
      .catch(err => {
        console.error('读取数据失败:', err);
        data.value = null;
      })
      .finally(() => {
        loading.value = false;
      });
  } else {
    // 精确模式：调用算法
    fetch('/api/run_algorithm', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        season: payload.season,
        penetration: payload.penetration,
        mode: 'accurate'
      })
    })
      .then(res => res.json())
      .then(d => {
        if (d.error) throw new Error(d.error);
        data.value = d;
      })
      .catch(err => {
        console.error('算法调用失败:', err);
        fallbackToCSV(payload);
      })
      .finally(() => {
        loading.value = false;
      });
  }
};

// 备选方案 
const fallbackToCSV = (payload) => {
  fetch(`/api/data?season=${payload.season}&penetration=${payload.penetration}`)
    .then(res => res.json())
    .then(d => {
      if (d.error) throw new Error(d.error);
      data.value = d;
    })
    .catch(err => {
      console.error(err);
      data.value = null;
    });
};
</script>

<style scoped>
/* 页面布局  */
.page-wrapper {
  background: #f0f4f8;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.page-content {
  flex: 1;
  padding: 24px 0 48px;
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

/* 控制行 */
.control-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px 20px;
  margin-top: 12px;
  padding: 12px 18px;
  background: white;
  border-radius: 12px;
  border: none !important;  
  box-shadow: none !important;
}

.control-row select,
.control-row button {
  border: 1px solid #e2e8f0 !important;
  outline: none !important;
  background: white;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 14px;
  color: #2c3e50;
}
.control-row select:focus,
.control-row button:focus {
  border-color: #e2e8f0 !important;
  box-shadow: none !important;
  outline: none !important;
}

/*  模式选项  */
.mode-options {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
  margin-left: 30px;  
}
.mode-option {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-size: 14px;
  color: #4a5568;
  user-select: none;
}
.mode-option input[type="checkbox"] {
  display: none;
}
.mode-option .checkmark {
  width: 18px;
  height: 18px;
  border: 2px solid #cbd5e0;
  border-radius: 4px;
  display: inline-block;
  position: relative;
  flex-shrink: 0;
  transition: all 0.2s;
  background: white;
}
.mode-option input[type="checkbox"]:checked + .checkmark {
  border-color: #2b6cb0;
  background: #2b6cb0;
}
.mode-option input[type="checkbox"]:checked + .checkmark::after {
  content: '';
  position: absolute;
  top: 2px;
  left: 6px;
  width: 6px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}
.mode-option:hover .checkmark {
  border-color: #a0aec0;
}

/*  取消按钮  */
.cancel-btn {
  padding: 4px 14px;
  border: 1px solid #e53e3e;
  border-radius: 6px;
  background: white;
  color: #e53e3e;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}
.cancel-btn:hover {
  background: #e53e3e;
  color: white;
}

.mode-hint {
  font-size: 12px;
  color: #a0aec0;
  margin-left: 4px;
  min-width: 120px;
}


.metric-cards {
  margin-top: 24px;     
  margin-bottom: 28px;  
}

.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 20px;
}
.scheme-section {
  margin-top: 32px;
  background: white;
  border-radius: 12px;
  padding: 20px 24px;
  border: 1px solid #eef2f7;
}
.scheme-section h3 {
  font-size: 18px;
  font-weight: 600;
  color: #0a1628;
  margin-bottom: 16px;
}
.loading-state {
  text-align: center;
  padding: 60px 0;
  color: #6b7a8f;
  font-size: 16px;
}
.empty-state {
  text-align: center;
  padding: 60px 0;
  color: #a0aec0;
}
@media (max-width: 900px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
}

/* 文字描述样式 */
.text-description {
  margin-bottom: 24px;
  padding: 16px 20px;
  background: #f8fafc;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
}
.text-description h4 {
  font-size: 15px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 12px;
}
.desc-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 8px;
  max-height: 400px;
  overflow-y: auto;
  padding-right: 4px;
}
.desc-grid::-webkit-scrollbar {
  width: 4px;
}
.desc-grid::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 4px;
}
.desc-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 13px;
  background: white;
  border-left: 3px solid #cbd5e0;
  transition: all 0.2s;
}
.desc-item:hover {
  transform: translateX(2px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.desc-item.charge {
  border-left-color: #e53e3e;
  background: #fff5f5;
}
.desc-item.discharge {
  border-left-color: #38a169;
  background: #f0fff4;
}
.desc-item.idle {
  border-left-color: #a0aec0;
  background: #f7fafc;
}
.desc-time {
  font-weight: 600;
  color: #2c3e50;
  min-width: 44px;
  font-size: 12px;
}
.desc-action {
  font-weight: 500;
  font-size: 12px;
  padding: 1px 8px;
  border-radius: 10px;
  min-width: 32px;
  text-align: center;
}
.charge .desc-action {
  background: #e53e3e;
  color: white;
}
.discharge .desc-action {
  background: #38a169;
  color: white;
}
.idle .desc-action {
  background: #a0aec0;
  color: white;
}
.desc-detail {
  color: #4a5568;
  font-size: 12px;
  flex: 1;
}

/* 调度计划概要 */
.schedule-summary {
  display: flex;
  flex-wrap: wrap;
  gap: 16px 32px;
  margin-top: 16px;
  padding-top: 14px;
  border-top: 1px dashed #e2e8f0;
}
.summary-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
}
.summary-label {
  color: #6b7a8f;
}
.summary-value {
  font-weight: 600;
  color: #0a1628;
}
</style>