<template>
  <section class="team-section">
    <div class="section-header">
      <h2 class="section-title">团队中心</h2>
      <p class="section-desc">展示已成立的优秀团队，支持招募队友与寻找团队</p>
      <router-link to="/team" class="view-all">查看全部 →</router-link>
    </div>
    <div class="team-grid">
      <div v-for="team in teams" :key="team.name" class="team-card">
        <div class="team-name">{{ team.name }}</div>
        <div class="team-members">
          <span v-for="m in team.members" :key="m.major" class="member">{{ m.major }}（{{ m.grade }}）</span>
        </div>
        <div class="skill-tags">
          <span v-for="s in team.skills" :key="s" class="skill">{{ s }}</span>
        </div>
        <div class="team-exp">过往项目数：{{ team.exp }}</div>
        <div class="team-actions">
          <router-link to="/team" class="btn-secondary">招募队友</router-link>
          <router-link to="/team" class="btn-primary">查看团队</router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const teams = [
  {
    name: '智农先锋',
    members: [
      { major: '计算机', grade: '2023' },
      { major: '农学', grade: '2022' },
      { major: '市场营销', grade: '2021' },
    ],
    skills: ['Python', '数据分析', '电商'],
    exp: 3,
  },
  {
    name: '文旅筑梦',
    members: [
      { major: '设计', grade: '2024' },
      { major: '传媒', grade: '2023' },
    ],
    skills: ['UI/UX', '短视频策划'],
    exp: 2,
  },
  {
    name: '医护连心',
    members: [
      { major: '公共卫生', grade: '2022' },
      { major: '软件工程', grade: '2023' },
    ],
    skills: ['后端', '数据可视化'],
    exp: 1,
  },
]
</script>

<style scoped>
.team-section {
  padding: 50px 5%;
  background: var(--color-bg, #f8f8f9);
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
  flex: 1;
}

.view-all {
  color: var(--color-accent, #c8102e);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
}

.team-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  max-width: var(--max-width, 1200px);
  margin: 0 auto;
}

.team-card {
  background: var(--color-card, #fff);
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
  width: 300px;
  transition: transform 0.25s;
}

.team-card:hover {
  transform: translateY(-3px);
}

.team-name {
  font-size: 18px;
  font-weight: 800;
  color: #222;
}

.team-members {
  font-size: 13px;
  color: var(--color-text-secondary, #6b6b6b);
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.skill-tags {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.skill {
  padding: 4px 10px;
  background: #f5f5f5;
  border-radius: 8px;
  font-size: 12px;
  color: #555;
}

.team-exp {
  margin-top: 8px;
  color: var(--color-text-secondary, #6b6b6b);
  font-size: 13px;
}

.team-actions {
  margin-top: 12px;
  display: flex;
  gap: 8px;
}

.btn-primary,
.btn-secondary {
  padding: 8px 14px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  transition: opacity 0.2s;
}

.btn-primary {
  background: var(--color-accent, #c8102e);
  color: #fff;
}

.btn-secondary {
  background: #fff;
  border: 1px solid #e6e6e6;
  color: #555;
}

.btn-primary:hover,
.btn-secondary:hover {
  opacity: 0.85;
}

@media (max-width: 768px) {
  .team-grid {
    flex-direction: column;
  }
  .team-card {
    width: 100%;
  }
}
</style>
