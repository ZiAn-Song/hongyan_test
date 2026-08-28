<template>
  <section class="practice-section">
    <div class="section-header">
      <h2 class="section-title-left">我发布的需求</h2>
      <div class="title-tag">管理面板</div>
    </div>

    <div class="manage-bar">
      <button class="publish-btn" @click="goPublish">
        <i class="fas fa-plus-circle"></i> 发布新需求
      </button>
    </div>

    <div class="demand-table">
      <div v-if="loading" class="loading-box">加载中...</div>
      <div v-else-if="demands.length === 0" class="empty-box">
        <i class="fas fa-inbox empty-icon"></i>
        <p>您还未发布任何需求</p>
        <button class="publish-btn" @click="goPublish">立即发布</button>
      </div>
      <table v-else>
        <thead>
          <tr>
            <th>需求标题</th>
            <th>实践地点</th>
            <th>预计周期</th>
            <th>状态</th>
            <th>发布时间</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="d in demands" :key="d.id" @click="goDemand">
            <td>{{ d.org_name || d.company_name }}</td>
            <td>{{ d.internship_location || '未指定' }}</td>
            <td>{{ d.estimated_time || '未指定' }}</td>
            <td>
              <span class="card-status" :class="d.status === 'open' ? 'status-open' : 'status-closed'">
                {{ d.status === 'open' ? '招募中' : '已关闭' }}
              </span>
            </td>
            <td>{{ formatDate(d.created_at) }}</td>
          </tr>
        </tbody>
      </table>
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

const formatDate = (dt) => {
  if (!dt) return '未知'
  return new Date(dt).toLocaleDateString('zh-CN')
}

const goPublish = () => router.push('/publish')
const goDemand = () => router.push('/demand')

const loadDemands = async () => {
  try {
    const res = await listDemands({ page: 1, page_size: 10 })
    demands.value = (res.items || []).filter(
      d => d.company_name === '当前企业'
    )
    if (demands.value.length === 0) demands.value = res.items || []
  } catch { demands.value = [] }
  loading.value = false
}

onMounted(loadDemands)
</script>

<style scoped>
.manage-bar {
  max-width: var(--max-width);
  margin: 0 auto 20px;
  display: flex;
  justify-content: flex-end;
}

.publish-btn {
  padding: 10px 24px;
  background: linear-gradient(135deg, var(--color-primary-dark), var(--color-primary));
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.publish-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(41, 128, 185, 0.3);
}

.demand-table {
  max-width: var(--max-width);
  margin: 0 auto;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
}

thead tr {
  background: linear-gradient(135deg, var(--color-primary-dark), var(--color-primary));
}

th {
  padding: 15px 20px;
  text-align: left;
  color: white;
  font-weight: 600;
  font-size: 0.95rem;
}

td {
  padding: 14px 20px;
  border-bottom: 1px solid #f0f0f0;
  font-size: 0.9rem;
  color: #555;
}

tbody tr {
  cursor: pointer;
  transition: background 0.2s;
}

tbody tr:hover {
  background: var(--paper-2);
}

tbody tr:last-child td {
  border-bottom: none;
}

.card-status {
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.status-open { background: rgba(47,107,79,.08); color: #2f6b4f; }
.status-closed { background: var(--color-accent-light); color: var(--color-accent); }

.loading-box, .empty-box {
  text-align: center;
  padding: 40px;
  color: #999;
}

.empty-icon {
  font-size: 3rem;
  color: #ddd;
  margin-bottom: 15px;
  display: block;
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
