<template>
  <footer class="app-footer">
    <div class="footer-content">
      <div class="footer-section">
        <h3>鸿雁平台</h3>
        <p>产学研融合助力边疆发展领航者</p>
        <p>连接地方需求，赋能边疆发展</p>
      </div>
      <div class="footer-section">
        <h3>快速链接</h3>
        <ul>
          <li><router-link to="/">网站首页</router-link></li>
          <li><router-link to="/publish">发布需求</router-link></li>
          <li><router-link to="/forum">论坛</router-link></li>
          <li><router-link to="/team">团队信息</router-link></li>
        </ul>
      </div>
      <div class="footer-section">
        <h3>联系我们</h3>
        <p><i class="fas fa-envelope"></i> contact@hongyan.edu.cn</p>
        <p><i class="fas fa-phone"></i> 010-XXXXXXXX</p>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2024 鸿雁 - 线上社会实践云平台 版权所有</p>
    </div>
  </footer>
</template>

<style scoped>
.app-footer {
  background: linear-gradient(135deg, #2c3e50, #1a252f);
  color: #ecf0f1;
  padding: 40px 5% 20px;
  margin-top: auto;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 30px;
  max-width: var(--max-width);
  margin: 0 auto 30px;
}

.footer-section h3 {
  font-size: 18px;
  margin-bottom: 15px;
  color: white;
}

.footer-section p {
  font-size: 14px;
  margin-bottom: 8px;
  color: #bdc3c7;
}

.footer-section p i {
  margin-right: 8px;
}

.footer-section ul li {
  margin-bottom: 8px;
}

.footer-section ul li a {
  color: #bdc3c7;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s;
}

.footer-section ul li a:hover {
  color: white;
}

.footer-bottom {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-bottom p {
  font-size: 13px;
  color: #95a5a6;
}
</style>
