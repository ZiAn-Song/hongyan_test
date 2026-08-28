<template>
  <footer class="app-footer">
    <div class="footer-rule"></div>
    <div class="footer-content">
      <div class="footer-brand">
        <p class="brand-name">鸿雁平台</p>
        <p class="brand-slogan">东西部协作 · 智能资源对接</p>
        <p class="brand-line">连接地方需求，赋能边疆发展</p>
      </div>
      <div class="footer-section">
        <h4>快速链接</h4>
        <ul>
          <li><router-link to="/">网站首页</router-link></li>
          <li><router-link to="/publish">发布需求</router-link></li>
          <li><router-link to="/forum">论坛</router-link></li>
          <li><router-link to="/team">团队信息</router-link></li>
        </ul>
      </div>
      <div class="footer-section">
        <h4>联系我们</h4>
        <ul>
          <li>contact@hongyan.edu.cn</li>
          <li>山东大学经济学院</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2026 鸿雁 · 东西部协作智能资源对接平台</p>
    </div>
  </footer>
</template>

<style scoped>
.app-footer {
  background: var(--paper-2);
  color: var(--ink-2);
  padding: 0 4% 22px;
  margin-top: auto;
  border-top: 1px solid var(--rule);
}

.footer-rule {
  border-top: 3px double var(--ink);
  max-width: var(--max-width);
  margin: 0 auto 30px;
  opacity: 0.55;
}

.footer-content {
  display: grid;
  grid-template-columns: 1.4fr 1fr 1fr;
  gap: 36px;
  max-width: var(--max-width);
  margin: 0 auto;
  padding-bottom: 26px;
}

.brand-name {
  font-family: var(--font-serif);
  font-size: 19px;
  font-weight: 700;
  letter-spacing: 3px;
  color: var(--ink);
}
.brand-slogan {
  font-size: 11px;
  letter-spacing: 2.5px;
  color: var(--color-primary);
  margin-top: 6px;
}
.brand-line { font-size: 12px; color: var(--ink-3); margin-top: 8px; }

.footer-section h4 {
  font-size: 12px;
  letter-spacing: 3px;
  color: var(--ink-3);
  text-transform: uppercase;
  margin-bottom: 12px;
  font-weight: 600;
}
.footer-section li { font-size: 13px; padding: 3px 0; color: var(--ink-2); }
.footer-section a:hover { color: var(--color-primary); }

.footer-bottom {
  border-top: 1px solid var(--rule);
  padding-top: 16px;
  text-align: center;
  font-size: 11px;
  letter-spacing: 2px;
  color: var(--ink-3);
}

@media (max-width: 760px) {
  .footer-content { grid-template-columns: 1fr; gap: 22px; }
}
</style>
