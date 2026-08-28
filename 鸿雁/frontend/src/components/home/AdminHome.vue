<template>
  <section class="practice-section">
    <div class="section-header">
      <h2 class="section-title-left">数据看板</h2>
      <div class="title-tag">管理员视角</div>
    </div>

    <div class="stats-grid">
      <div v-for="s in stats" :key="s.label" class="stat-card" :style="{ '--card-color': s.color }">
        <i :class="s.icon"></i>
        <div class="stat-info">
          <div class="stat-value">{{ s.value }}</div>
          <div class="stat-label">{{ s.label }}</div>
        </div>
      </div>
    </div>
  </section>

  <section class="practice-section">
    <div class="section-header">
      <h2 class="section-title-left">管理入口</h2>
      <div class="title-tag">快捷操作</div>
    </div>

    <div class="manage-grid">
      <div class="manage-card" @click="goCrawler">
        <i class="fas fa-rss"></i>
        <h3>爬虫管理</h3>
        <p>手动采集边疆资讯</p>
      </div>
      <div class="manage-card" @click="goTeam">
        <i class="fas fa-users"></i>
        <h3>团队管理</h3>
        <p>查看所有实践团队</p>
      </div>
      <div class="manage-card" @click="goDemand">
        <i class="fas fa-bullhorn"></i>
        <h3>需求管理</h3>
        <p>查看所有发布需求</p>
      </div>
      <div class="manage-card" @click="goForum">
        <i class="fas fa-comments"></i>
        <h3>论坛管理</h3>
        <p>查看论坛帖子</p>
      </div>
    </div>
  </section>

  <section class="practice-section">
    <div class="section-header">
      <h2 class="section-title-left">行动进行时</h2>
      <div class="title-tag">最新发布</div>
    </div>
    <div class="practice-container">
      <ActivityList />
      <ImageCarousel />
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ActivityList from './ActivityList.vue'
import ImageCarousel from './ImageCarousel.vue'

const router = useRouter()

const stats = ref([
  { label: '爬取资讯', value: '...', icon: 'fas fa-rss', color: 'var(--color-primary)' },
  { label: '实践团队', value: '...', icon: 'fas fa-users', color: 'var(--el-color-success)' },
  { label: '发布需求', value: '...', icon: 'fas fa-bullhorn', color: 'var(--el-color-warning)' },
  { label: '论坛帖子', value: '...', icon: 'fas fa-comments', color: '#8e44ad' },
])

const goCrawler = () => router.push('/crawler')
const goTeam = () => router.push('/team')
const goDemand = () => router.push('/demand')
const goForum = () => router.push('/forum')

onMounted(async () => {
  try {
    const [crawlRes, teamRes, demandRes] = await Promise.allSettled([
      fetch('/api/crawler/articles?page=1&page_size=1').then(r => r.json()),
      fetch('/api/teams/?page=1&page_size=1').then(r => r.json()),
      fetch('/api/demands/?page=1&page_size=1').then(r => r.json()),
    ])
    if (crawlRes.status === 'fulfilled') stats.value[0].value = crawlRes.value.total ?? 0
    if (teamRes.status === 'fulfilled') stats.value[1].value = teamRes.value.total ?? 0
    if (demandRes.status === 'fulfilled') stats.value[2].value = demandRes.value.total ?? 0
  } catch {}
})
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
  max-width: var(--max-width);
  margin: 0 auto;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  border-left: 6px solid var(--card-color);
  transition: transform 0.3s, box-shadow 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.12);
}

.stat-card i {
  font-size: 2.5rem;
  color: var(--card-color);
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: var(--ink);
}

.stat-label {
  font-size: 0.9rem;
  color: #999;
  margin-top: 4px;
}

.manage-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  max-width: var(--max-width);
  margin: 0 auto;
}

.manage-card {
  background: white;
  border-radius: 12px;
  padding: 30px 25px;
  text-align: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  border-top: 4px solid var(--color-primary);
}

.manage-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.12);
}

.manage-card i {
  font-size: 2.5rem;
  color: var(--color-primary);
  margin-bottom: 15px;
}

.manage-card h3 {
  font-size: 1.2rem;
  color: var(--ink);
  margin-bottom: 8px;
}

.manage-card p {
  color: #999;
  font-size: 0.9rem;
}

.practice-section {
  padding: 50px 5%;
  background-color: var(--color-bg-card);
}

.section-header {
  margin-bottom: 25px;
  max-width: var(--max-width);
  margin-left: auto;
  margin-right: auto;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.section-title-left {
  font-size: 26px;
  color: var(--color-accent-dark);
  font-weight: 600;
  position: relative;
  padding-bottom: 10px;
  margin-bottom: 6px;
}

.section-title-left::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background-color: var(--color-accent);
}

.title-tag {
  color: var(--color-accent);
  font-weight: 500;
  background-color: var(--color-accent-light);
  padding: 4px 10px;
  border-radius: 18px;
  font-size: 12px;
}

.practice-container {
  display: flex;
  gap: 30px;
  max-width: var(--max-width);
  margin: 0 auto;
}

@media (max-width: 1024px) {
  .practice-container {
    flex-direction: column;
    gap: 30px;
  }
}
</style>
