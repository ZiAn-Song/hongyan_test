<template>
  <section class="support-section">
    <div class="section-header">
      <h2 class="section-title">后端支撑点（线下网络）</h2>
      <p class="section-desc">山东大学在各地建立的研究院、技术转移中心、校友会、合作企业等线下实体</p>
    </div>
    <div class="support-grid">
      <div v-for="base in bases" :key="base.name" class="base-card">
        <div class="base-icon"><i :class="base.icon"></i></div>
        <div class="base-name">{{ base.name }}</div>
        <div class="base-focus">聚焦：{{ base.focus }}</div>
        <div class="base-support">支持：{{ base.support }}</div>
      </div>
    </div>
  </section>
</template>

<script setup>
const bases = [
  { name: '烟台研究院', focus: '智慧海洋·海洋经济', support: '办公空间、导师支持', icon: 'fas fa-anchor' },
  { name: '菏泽校友会', focus: '农业技术推广', support: '渠道对接', icon: 'fas fa-seedling' },
  { name: '济南技术转移中心', focus: '技术孵化', support: '专利咨询、融资对接', icon: 'fas fa-industry' },
]
</script>

<style scoped>
.support-section {
  padding: 50px 5%;
  background: var(--color-bg, #f8f8f9);
}

.section-header {
  max-width: var(--max-width, 1200px);
  margin: 0 auto 25px;
}

.section-title {
  font-size: 26px;
  color: var(--color-accent-dark, #c8102e);
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
  background: var(--color-accent, #c8102e);
}

.section-desc {
  color: var(--color-text-secondary, #6b6b6b);
  font-size: 14px;
}

.support-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
  max-width: var(--max-width, 1200px);
  margin: 0 auto;
}

.base-card {
  background: var(--color-card, #fff);
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
  text-align: center;
  transition: transform 0.25s;
}

.base-card:hover {
  transform: translateY(-3px);
}

.base-icon {
  font-size: 32px;
  color: var(--color-accent, #c8102e);
  margin-bottom: 12px;
}

.base-name {
  font-size: 16px;
  font-weight: 700;
  color: #222;
}

.base-focus {
  color: var(--color-text-secondary, #6b6b6b);
  font-size: 13px;
  margin-top: 8px;
}

.base-support {
  color: var(--color-text-secondary, #6b6b6b);
  font-size: 13px;
  margin-top: 4px;
}
</style>
