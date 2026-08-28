<template>
  <footer class="footer">
    <div class="container">
      <p>© 2026 智能电网实时模拟平台 · 基于 IBWO-MOMPA 双算法协同优化</p>
      <p class="footer-links">
        <a href="#" @click.prevent>隐私政策</a>
        <span class="divider">|</span>
        <a href="#" @click.prevent>联系我们</a>
      </p>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: #0a1628;
  padding: 24px 0;
  text-align: center;
  margin-top: auto;
}
.footer p {
  color: #6b7a8f;
  font-size: 13px;
  margin: 4px 0;
}
.footer-links {
  display: flex;
  justify-content: center;
  gap: 12px;
  align-items: center;
}
.footer-links a {
  color: #6b7a8f;
  font-size: 13px;
  text-decoration: none;
}
.footer-links a:hover {
  color: #a0aec0;
}
.divider {
  color: #2d3748;
}
</style>