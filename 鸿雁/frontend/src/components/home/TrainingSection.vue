<template>
  <section class="training-section">
    <div class="section-header">
      <h2 class="section-title">培训赋能站</h2>
      <p class="section-desc">AI 导师、校内导师与企业专家联合出品的系列课程、常见问题与优秀案例库</p>
    </div>
    <div class="course-grid">
      <div v-for="course in courses" :key="course.title" class="course-card">
        <div class="course-icon"><i :class="course.icon"></i></div>
        <div class="course-title">{{ course.title }}</div>
        <div class="course-meta">{{ course.author }} · {{ course.duration }}</div>
        <button class="btn-primary">进入课程</button>
      </div>
    </div>
  </section>
</template>

<script setup>
const courses = [
  { title: '项目管理与进度控制', author: '校内导师', duration: '2h', icon: 'fas fa-tasks' },
  { title: '乡村调研方法论', author: '企业专家', duration: '1.5h', icon: 'fas fa-clipboard-list' },
  { title: '数据安全与隐私保护', author: '信息中心', duration: '1h', icon: 'fas fa-shield-alt' },
  { title: '孵化与成果转化指南', author: '技术转移中心', duration: '2h', icon: 'fas fa-lightbulb' },
]
</script>

<style scoped>
.training-section {
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

.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  max-width: var(--max-width, 1200px);
  margin: 0 auto;
}

.course-card {
  background: linear-gradient(180deg, #fff, #fbfbff);
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
  text-align: center;
  transition: transform 0.25s;
}

.course-card:hover {
  transform: translateY(-3px);
}

.course-icon {
  font-size: 32px;
  color: var(--color-accent, #c8102e);
  margin-bottom: 12px;
}

.course-title {
  font-size: 16px;
  font-weight: 700;
  color: #222;
}

.course-meta {
  color: var(--color-text-secondary, #6b6b6b);
  font-size: 13px;
  margin-top: 6px;
  margin-bottom: 14px;
}

.btn-primary {
  padding: 8px 16px;
  border-radius: 8px;
  border: none;
  background: var(--color-accent, #c8102e);
  color: #fff;
  font-weight: 600;
  font-size: 13px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-primary:hover {
  opacity: 0.85;
}
</style>
