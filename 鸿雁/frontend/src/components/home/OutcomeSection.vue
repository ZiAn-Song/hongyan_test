<template>
  <section class="outcome-section">
    <div class="section-header">
      <h2 class="section-title">成果展示</h2>
      <p class="section-desc">历年优秀项目的报告、代码、演示、论文、专利、媒体报道等</p>
      <router-link to="/achievement" class="view-all">查看全部 →</router-link>
    </div>
    <div class="outcome-grid">
      <div v-for="item in outcomes" :key="item.title" class="outcome-card">
        <div class="outcome-icon"><i :class="item.icon"></i></div>
        <div class="outcome-title">{{ item.title }}</div>
        <div class="outcome-meta">{{ item.meta }}</div>
        <router-link to="/achievement" class="outcome-link">查看详情</router-link>
      </div>
    </div>
  </section>
</template>

<script setup>
const outcomes = [
  { title: '农村电商助手 · 项目报告', meta: '软件/演示/论文', icon: 'fas fa-file-alt' },
  { title: '数字文旅样例站点', meta: '网站/演示', icon: 'fas fa-globe' },
  { title: '远程诊疗系统调研报告', meta: '报告/调研', icon: 'fas fa-notes-medical' },
]
</script>

<style scoped>
.outcome-section {
  padding: 50px 5%;
  background: var(--color-bg-card, #f8f8f9);
}

.section-header {
  max-width: var(--max-width, 1200px);
  margin: 0 auto 25px;
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 8px;
}

.section-title {
  font-size: 26px;
  color: var(--color-accent-dark, #16305c);
  font-weight: 700;
  margin-bottom: 6px;
  position: relative;
  padding-bottom: 10px;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background: var(--color-accent, #16305c);
}

.section-desc {
  color: var(--color-text-secondary, #6b6b6b);
  font-size: 14px;
  flex: 1;
}

.view-all {
  color: var(--color-accent, #16305c);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
}

.outcome-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
  max-width: var(--max-width, 1200px);
  margin: 0 auto;
}

.outcome-card {
  background: var(--color-card, #fff);
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
  text-align: center;
  transition: transform 0.25s;
}

.outcome-card:hover {
  transform: translateY(-3px);
}

.outcome-icon {
  font-size: 32px;
  color: var(--color-accent, #16305c);
  margin-bottom: 12px;
}

.outcome-title {
  font-size: 16px;
  font-weight: 700;
  color: #222;
}

.outcome-meta {
  color: var(--color-text-secondary, #6b6b6b);
  font-size: 13px;
  margin-top: 6px;
  margin-bottom: 14px;
}

.outcome-link {
  color: var(--color-accent, #16305c);
  text-decoration: none;
  font-size: 13px;
  font-weight: 600;
}

.outcome-link:hover {
  text-decoration: underline;
}
</style>
