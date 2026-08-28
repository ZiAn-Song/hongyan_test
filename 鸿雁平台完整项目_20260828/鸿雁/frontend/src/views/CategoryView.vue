<template>
  <div class="page">
    <AppHeader />

    <div class="category-page">
      <header class="category-header" :style="headerStyle">
        <h1>
          <i :class="categoryConfig.icon"></i>
          {{ categoryConfig.title }}
          <i :class="categoryConfig.iconEnd" v-if="categoryConfig.iconEnd"></i>
        </h1>
        <p>{{ categoryConfig.description }}</p>
      </header>

      <div v-if="loading" class="loading">
        <div class="spinner" :style="{ borderTopColor: categoryConfig.color }"></div>
        <p>正在加载{{ categoryConfig.title }}项目数据...</p>
      </div>

      <div v-else-if="error" class="error">
        <i class="fas fa-exclamation-triangle error-icon"></i>
        <p>{{ error }}</p>
        <button class="retry-btn" :style="{ background: categoryConfig.color }" @click="loadData">
          重新加载
        </button>
      </div>

      <div v-else-if="projects.length === 0" class="no-data">
        <i class="fas fa-clipboard-list no-data-icon"></i>
        <h3>暂无{{ categoryConfig.title }}相关项目</h3>
        <p>当前没有机构发布{{ categoryConfig.title }}领域的实践需求</p>
      </div>

      <main v-else class="job-listings">
        <article
          v-for="(project, index) in projects"
          :key="index"
          class="job-card"
          :style="{ borderLeftColor: categoryConfig.color }"
        >
          <h2 class="job-title" :style="{ color: categoryConfig.color }">
            <span class="job-icon">📋</span>
            {{ project.companyName }}
            <span class="status-tag" :style="{ backgroundColor: categoryConfig.lightColor, color: categoryConfig.color }">
              {{ categoryConfig.shortTitle }}
            </span>
          </h2>

          <div class="job-location-salary">
            <div class="location"><span>📍</span> {{ project.location }}</div>
            <div class="salary">{{ project.estimatedTime }}</div>
          </div>

          <div class="requirements">
            <div class="requirement-item" :style="{ color: categoryConfig.color }">{{ project.orgType }}</div>
            <div class="requirement-item" :style="{ color: categoryConfig.color }">{{ project.estimatedTime }}</div>
            <div class="requirement-item" :style="{ color: categoryConfig.color }">{{ categoryConfig.shortTitle }}相关专业</div>
          </div>

          <div class="job-description">
            <p>{{ project.requirements }}</p>
          </div>

          <div class="company-info">
            <div class="company-details">
              <span class="company-name" :style="{ color: categoryConfig.color }">{{ project.companyName }}</span>
              <div class="company-tags">
                <span class="company-tag" :style="{ backgroundColor: categoryConfig.lightColor, color: categoryConfig.color }">{{ categoryConfig.shortTitle }}</span>
                <span class="company-tag" :style="{ backgroundColor: categoryConfig.lightColor, color: categoryConfig.color }">{{ project.orgType }}</span>
                <span class="company-tag" :style="{ backgroundColor: categoryConfig.lightColor, color: categoryConfig.color }">社会实践</span>
              </div>
            </div>
            <button class="apply-btn" :style="applyBtnStyle" @click="applyForProject(project.companyName)">
              报名加入
            </button>
          </div>
        </article>

        <hr v-if="projects.length > 1" class="divider" :style="{ background: `linear-gradient(to right, transparent, ${categoryConfig.color}, transparent)` }" />
      </main>

      <div v-if="totalPages > 1 && !loading && !error" class="pagination-container">
        <div class="pagination">
          <button
            class="page-btn"
            :class="{ disabled: currentPage === 1 }"
            @click="changePage(currentPage - 1)"
          >
            <i class="fas fa-chevron-left"></i>
          </button>
          <span class="page-info">第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
          <button
            class="page-btn"
            :class="{ disabled: currentPage === totalPages }"
            @click="changePage(currentPage + 1)"
          >
            <i class="fas fa-chevron-right"></i>
          </button>
        </div>
      </div>

      <div class="page-footer">
        <p>山东大学实践服务平台 - {{ categoryConfig.title }}领域</p>
        <p class="footer-hint">数据来源于政企机构提交的实践需求，实时更新</p>
      </div>
    </div>

    <AppFooter />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import { listDemands } from '@/api/demands'

const route = useRoute()

const categoryMap = {
  healthcare: {
    title: '医疗健康',
    shortTitle: '医疗健康',
    description: '浏览医疗机构、健康部门发布的实践需求，寻找适合您的项目机会',
    icon: 'fas fa-heartbeat',
    iconEnd: 'fas fa-stethoscope',
    color: '#1a8c6d',
    lightColor: '#e6f7f2',
    filter: '医疗健康'
  },
  infrastructure: {
    title: '基础建设',
    shortTitle: '基础建设',
    description: '浏览基础建设相关机构发布的实践需求，参与边疆基础设施建设',
    icon: 'fas fa-hard-hat',
    iconEnd: '',
    color: 'var(--el-color-warning)',
    lightColor: '#fef3e6',
    filter: '基础建设'
  },
  education: {
    title: '教育民生',
    shortTitle: '教育民生',
    description: '浏览教育机构发布的实践需求，助力边疆教育发展',
    icon: 'fas fa-graduation-cap',
    iconEnd: '',
    color: 'var(--color-primary)',
    lightColor: '#ebf5fb',
    filter: '教育民生'
  },
  grassroots: {
    title: '基层治理',
    shortTitle: '基层治理',
    description: '浏览基层治理相关实践需求，参与社区治理与公共服务',
    icon: 'fas fa-people-group',
    iconEnd: '',
    color: '#8e44ad',
    lightColor: '#f4ecf7',
    filter: '基层治理'
  },
  culture: {
    title: '文旅',
    shortTitle: '文旅',
    description: '浏览文旅相关实践需求，促进文化旅游产业发展',
    icon: 'fas fa-mountain-sun',
    iconEnd: '',
    color: '#16a085',
    lightColor: '#e8f8f5',
    filter: '文旅'
  },
  environment: {
    title: '环境',
    shortTitle: '环境',
    description: '浏览环保相关实践需求，参与生态环境保护与可持续发展',
    icon: 'fas fa-leaf',
    iconEnd: '',
    color: 'var(--el-color-success)',
    lightColor: '#e9f7ef',
    filter: '环境'
  }
}

const chineseToKey = {
  '医疗健康': 'healthcare',
  '基础建设': 'infrastructure',
  '教育民生': 'education',
  '基层治理': 'grassroots',
  '文旅': 'culture',
  '环境': 'environment'
}

const categoryConfig = computed(() => {
  const type = route.params.type || 'healthcare'
  const key = chineseToKey[type] || type
  return categoryMap[key] || categoryMap.healthcare
})

const headerStyle = computed(() => ({
  background: `linear-gradient(135deg, ${categoryConfig.value.color} 0%, ${categoryConfig.value.color}dd 100%)`,
  boxShadow: `0 10px 25px ${categoryConfig.value.color}40`
}))

const applyBtnStyle = computed(() => ({
  background: `linear-gradient(135deg, ${categoryConfig.value.color} 0%, ${categoryConfig.value.color}dd 100%)`,
  boxShadow: `0 5px 15px ${categoryConfig.value.color}4d`
}))

const projects = ref([])
const total = ref(0)
const totalPages = ref(1)
const loading = ref(true)
const error = ref('')
const currentPage = ref(1)
const itemsPerPage = 4

function truncate(text, max) {
  if (!text) return ''
  if (text.length <= max) return text
  return text.substring(0, max) + '...'
}

const loadData = async () => {
  loading.value = true
  error.value = ''

  try {
    const result = await listDemands({
      category: categoryConfig.value.filter,
      page: currentPage.value,
      page_size: itemsPerPage
    })
    projects.value = (result.items || []).map(p => ({
      companyName: p.org_name || p.company_name || '未知机构',
      location: p.internship_location || '地点待定',
      estimatedTime: p.estimated_time || '时间待定',
      requirements: truncate(p.requirements_content || '暂无详细需求', 200),
      orgType: p.org_type || '机构'
    }))
    total.value = result.total || 0
    totalPages.value = result.total_pages || 1
  } catch (err) {
    console.error('加载数据失败:', err)
    error.value = `数据加载失败: ${err.message || '请稍后重试'}`
  } finally {
    loading.value = false
  }
}

const changePage = (page) => {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
  loadData()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const applyForProject = (companyName) => {
  ElMessage.success(`您已申请加入 "${companyName}" 的${categoryConfig.value.title}项目，平台管理员会尽快与您联系！`)
}

watch(() => route.params.type, () => {
  currentPage.value = 1
  loadData()
})

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.category-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.category-header {
  color: white;
  padding: 40px 30px;
  border-radius: 15px;
  margin-bottom: 40px;
  text-align: center;
}

.category-header h1 {
  font-size: 2.8rem;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.category-header p {
  font-size: 1.2rem;
  opacity: 0.9;
  max-width: 800px;
  margin: 0 auto;
}

.job-listings {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.job-card {
  background-color: var(--color-bg-card);
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  border-left: 6px solid;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.job-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.12);
}

.job-title {
  font-size: 1.8rem;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.job-icon {
  font-size: 1.5rem;
}

.status-tag {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: bold;
  margin-left: 10px;
}

.job-location-salary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--color-border);
}

.location {
  font-size: 1.1rem;
  color: #555;
  display: flex;
  align-items: center;
  gap: 8px;
}

.salary {
  font-size: 1.4rem;
  color: #e63946;
  font-weight: bold;
}

.requirements {
  display: flex;
  gap: 30px;
  margin-bottom: 25px;
  flex-wrap: wrap;
}

.requirement-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1rem;
  font-weight: 500;
}

.requirement-item::before {
  content: "•";
  font-weight: bold;
  font-size: 1.2rem;
}

.company-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 20px;
  border-top: 1px dashed #ddd;
}

.company-details {
  display: flex;
  align-items: center;
  gap: 15px;
}

.company-name {
  font-size: 1.3rem;
  font-weight: bold;
}

.company-tags {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.company-tag {
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
}

.apply-btn {
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 30px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.2s;
}

.apply-btn:hover {
  transform: translateY(-2px);
}

.divider {
  height: 2px;
  margin: 30px 0;
  border: none;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #666;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  text-align: center;
  padding: 40px;
  color: #e63946;
  background-color: var(--color-primary-light);
  border-radius: 10px;
  margin: 20px 0;
}

.error-icon {
  font-size: 2rem;
  margin-bottom: 15px;
}

.retry-btn {
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 15px;
}

.no-data {
  text-align: center;
  padding: 40px;
  color: #666;
  font-style: italic;
}

.no-data-icon {
  font-size: 3rem;
  margin-bottom: 15px;
  color: #ddd;
}

.job-description {
  margin-bottom: 25px;
  color: #555;
  line-height: 1.7;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 40px;
}

.pagination {
  display: flex;
  gap: 10px;
  align-items: center;
}

.page-btn {
  padding: 8px 16px;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.95rem;
  min-width: 40px;
  text-align: center;
}

.page-btn:hover:not(.disabled) {
  background-color: #f5f5f5;
}

.page-btn.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: #666;
  font-size: 0.9rem;
  margin: 0 15px;
}

.page-footer {
  text-align: center;
  margin-top: 50px;
  padding-top: 20px;
  border-top: 1px solid #d9e7ff;
  color: #666;
  font-size: 0.9rem;
}

.footer-hint {
  margin-top: 10px;
  font-size: 0.85rem;
}

@media (max-width: 768px) {
  .category-header h1 {
    font-size: 2.2rem;
    flex-direction: column;
    gap: 10px;
  }

  .job-location-salary {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .requirements {
    flex-direction: column;
    gap: 10px;
  }

  .company-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }

  .apply-btn {
    align-self: stretch;
    text-align: center;
  }

  .pagination {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>
