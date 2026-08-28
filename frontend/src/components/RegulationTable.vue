<template>
  <div class="table-wrapper">
    <div v-if="data.length === 0" class="empty">暂无数据</div>
    <table v-else class="regulation-table">
      <thead>
        <tr>
          <th>时段</th>
          <th>储能功率<br><span class="sub">(MW)</span></th>
          <th>储能SOC</th>
          <th>OLTC档位</th>
          <th>SVC出力<br><span class="sub">(Mvar)</span></th>
          <th>17号电容</th>
          <th>29号电容</th>
          <th>32号电容</th>
          <th>需求响应比</th>
        </tr>
      </thead>
      <tbody>
      <tr v-for="row in data" :key="row['时段']">
          <td class="col-hour">{{ row['时段'] }}</td>
          <td :class="row['储能功率(MW)'] >= 0 ? 'discharge' : 'charge'">
            {{ row['储能功率(MW)']?.toFixed(3) || '0.000' }}
          </td>
          <td>{{ row['储能SOC']?.toFixed(3) || '0.000' }}</td>
          <td>{{ row['OLTC分接头档位'] || 0 }}</td>
          <td>{{ row['SVC无功容量(Mvar)']?.toFixed(3) || '0.000' }}</td>
          <td>{{ row['17号电容器投切档位'] || 0 }}</td>
          <td>{{ row['29号电容器投切档位'] || 0 }}</td>
          <td>{{ row['32号电容器投切档位'] || 0 }}</td>
          <td>{{ ((row['需求响应比例'] || 0) * 100).toFixed(1) }}%</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  data: { type: Array, required: true }
});
</script>

<style scoped>
.table-wrapper {
  overflow-x: auto;
}
.regulation-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  min-width: 900px;
}
.regulation-table th {
  background: #f8fafc;
  padding: 10px 12px;
  text-align: center;
  border-bottom: 2px solid #e2e8f0;
  font-weight: 600;
  color: #2c3e50;
}
.regulation-table th .sub {
  font-weight: 400;
  font-size: 11px;
  color: #6b7a8f;
}
.regulation-table td {
  padding: 8px 12px;
  text-align: center;
  border-bottom: 1px solid #f0f4f8;
  font-family: 'Courier New', monospace;
  font-size: 13px;
}
.regulation-table tr:hover td {
  background: #f7fafc;
}
.col-hour {
  font-weight: 600;
  color: #2c3e50;
  font-family: inherit;
}
.charge {
  color: #e53e3e;
}
.discharge {
  color: #38a169;
}
.empty {
  padding: 20px;
  text-align: center;
  color: #a0aec0;
}
</style>