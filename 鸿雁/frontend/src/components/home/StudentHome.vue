<template>
  <section class="practice-section">
    <div class="section-header">
      <h2 class="section-title-left">需求推荐</h2>
      <div class="title-tag">为你精选</div>
    </div>
    <div class="demand-cards">
      <div v-if="loading" class="loading-box">加载中...</div>
      <div v-else-if="demands.length === 0" class="empty-box">暂无推荐需求</div>
      <div v-else class="card-grid">
        <div v-for="d in demands" :key="d.id" class="demand-card" @click="goDemand(d.id)">
          <div class="card-header">
            <span class="card-org">{{ d.org_name || d.company_name }}</span>
            <span class="card-status" :class="d.status === 'open' ? 'status-open' : 'status-closed'">
              {{ d.status === 'open' ? '招募中' : '已关闭' }}
            </span>
          </div>
          <div class="card-location"><i class="fas fa-map-marker-alt"></i> {{ d.internship_location || '未指定' }}</div>
          <div class="card-majors">
            <span v-for="(m, i) in (d.target_majors || []).slice(0, 3)" :key="i" class="major-chip">{{ m }}</span>
          </div>
          <p class="card-desc">{{ truncate(d.requirements_content, 80) }}</p>
        </div>
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
import { listDemands } from '@/api/demands'
import ActivityList from './ActivityList.vue'
import ImageCarousel from './ImageCarousel.vue'

const router = useRouter()
const demands = ref([])
const loading = ref(true)

const truncate = (text, n) => {
  if (!text) return ''
  return text.length > n ? text.slice(0, n) + '...' : text
}

const goDemand = (id) => router.push('/demand')

const loadDemands = async () => {
  try {
    const res = await listDemands({ page: 1, page_size: 4 })
    demands.value = res.items || []
  } catch { demands.value = [] }
  loading.value = false
}

onMounted(loadDemands)
</script>

<style scoped>
.demand-cards {
  max-width: var(--max-width);
  margin: 0 auto;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.demand-card {
  background: var(--color-bg-card);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  border-left: 5px solid var(--color-primary);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.demand-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.12);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.card-org {
  font-size: 1.1rem;
  font-weight: bold;
  color: var(--color-primary);
}

.card-status {
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.status-open { background: rgba(47,107,79,.08); color: #2f6b4f; }
.status-closed { background: var(--color-accent-light); color: var(--color-accent); }

.card-location {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 10px;
}

.card-majors {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-bottom: 10px;
}

.major-chip {
  background: var(--color-accent-light);
  color: var(--color-accent-dark);
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.8rem;
}

.card-desc {
  color: #555;
  font-size: 0.9rem;
  line-height: 1.5;
}

.loading-box, .empty-box {
  text-align: center;
  padding: 40px;
  color: #999;
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
