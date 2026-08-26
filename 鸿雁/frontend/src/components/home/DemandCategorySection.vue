<template>
  <section class="demand-section">
    <div class="section-header">
      <h2 class="section-title">需求分类</h2>
      <p class="section-desc">按领域浏览边疆地区亟待解决的需求</p>
    </div>
    <div class="category-grid">
      <router-link
        v-for="cat in categories"
        :key="cat.name"
        :to="cat.link"
        class="category-card"
        :style="{ '--cat-color': cat.color, '--cat-bg': cat.bg }"
      >
        <i :class="cat.icon"></i>
        <span class="cat-name">{{ cat.name }}</span>
      </router-link>
    </div>
  </section>
</template>

<script setup>
const categories = [
  { name: '医疗健康', icon: 'fas fa-heartbeat', color: '#1d71b8', bg: 'linear-gradient(135deg, #f0f7ff, #e6f0ff)', link: '/category?key=health' },
  { name: '基础建设', icon: 'fas fa-hard-hat', color: '#2c9c6b', bg: 'linear-gradient(135deg, #f0fff4, #e6ffec)', link: '/category?key=infrastructure' },
  { name: '教育民生', icon: 'fas fa-graduation-cap', color: '#e67e22', bg: 'linear-gradient(135deg, #fff8f0, #fff0e6)', link: '/category?key=education' },
  { name: '基层治理', icon: 'fas fa-landmark', color: '#9b59b6', bg: 'linear-gradient(135deg, #f8f0ff, #f0e6ff)', link: '/category?key=governance' },
  { name: '文旅', icon: 'fas fa-mountain', color: '#c8102e', bg: 'linear-gradient(135deg, #fff0f5, #ffe6ee)', link: '/category?key=tourism' },
  { name: '环境', icon: 'fas fa-leaf', color: '#1a8a5b', bg: 'linear-gradient(135deg, #f0fff8, #e6fff0)', link: '/category?key=environment' },
]
</script>

<style scoped>
.demand-section {
  padding: 50px 5%;
  background: var(--color-bg-card, #f8f8f9);
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

.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  max-width: var(--max-width, 1200px);
  margin: 0 auto;
}

.category-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 28px 16px;
  background: var(--cat-bg);
  border-radius: 12px;
  text-decoration: none;
  color: var(--cat-color);
  font-weight: 600;
  font-size: 18px;
  transition: transform 0.25s, box-shadow 0.25s;
}

.category-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.category-card i {
  font-size: 36px;
}

@media (max-width: 768px) {
  .category-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .category-card {
    padding: 20px 12px;
    font-size: 16px;
  }
  .category-card i {
    font-size: 28px;
  }
}
</style>
