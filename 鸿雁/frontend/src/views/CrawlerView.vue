<template>
  <div class="page">
    <AppHeader />

    <div class="crawler-page">
      <header class="page-banner">
        <div class="banner-content">
          <h1><i class="fas fa-rss"></i> 边疆资讯</h1>
          <p>定期从民政部、新华社、国家民委、发改委、工信部、中国政府网、边疆研究所等官方信源自动采集</p>
        </div>
      </header>

      <div class="content-wrapper">
        <div class="toolbar">
          <div class="search-box">
            <i class="fas fa-search search-icon"></i>
            <input
              v-model="searchKeyword"
              type="text"
              placeholder="搜索标题、内容、关键词..."
              class="search-input"
              @keyup.enter="handleSearch"
            />
          </div>
          <select v-model="filterSource" class="filter-select" @change="handleSearch">
            <option value="">全部信源</option>
            <option v-for="s in sources" :key="s.key" :value="s.key">{{ s.name }}</option>
          </select>
          <input
            v-model="filterDateStart"
            type="date"
            class="date-input"
            @change="handleSearch"
          />
          <span class="date-sep">至</span>
          <input
            v-model="filterDateEnd"
            type="date"
            class="date-input"
            @change="handleSearch"
          />
          <button v-if="authStore.isAdmin" class="trigger-btn" :disabled="crawling" @click="handleTrigger">
            <i class="fas fa-sync-alt" :class="{ 'fa-spin': crawling }"></i>
            {{ crawling ? '采集中...' : '手动采集' }}
          </button>
          <button
            v-if="authStore.isLoggedIn && articles.length > 0"
            class="clear-btn"
            :disabled="clearing"
            @click="handleClearAll"
          >
            <i class="fas fa-trash-alt"></i>
            {{ clearing ? '清理中...' : '清空数据' }}
          </button>
        </div>

        <!-- 最新爬取区域 -->
        <div v-if="!todayLoading && todayArticles.length > 0" class="today-section">
          <div class="today-header">
            <div class="today-title">
              <i class="fas fa-bolt"></i>
              <span>最新爬取</span>
              <span class="today-date">{{ todayLabel }}</span>
            </div>
            <span class="today-count">今日采集 {{ todayArticles.length }} 篇</span>
          </div>
          <div class="today-scroll">
            <article
              v-for="item in todayArticles"
              :key="item.id"
              class="today-card"
              @click="openDetail(item)"
            >
              <span class="source-badge" :class="sourceClass(item.source)">{{ item.source }}</span>
              <h3 class="today-card-title">{{ item.title }}</h3>
              <p class="today-card-summary" v-if="item.summary">{{ truncateText(item.summary, 80) }}</p>
              <span class="today-card-time" v-if="item.publish_date">
                <i class="fas fa-clock"></i> {{ formatTime(item.publish_date) }}
              </span>
            </article>
          </div>
        </div>

        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          <p>正在加载资讯...</p>
        </div>

        <div v-else-if="articles.length === 0" class="no-data">
          <i class="fas fa-folder-open no-data-icon"></i>
          <p>暂无采集到的资讯</p>
          <p class="no-data-hint" v-if="authStore.isAdmin">点击"手动采集"按钮开始爬取</p>
        </div>

        <div v-else class="article-list">
          <div v-for="group in groupedArticles" :key="group.key" class="date-group">
            <div class="date-group-header">
              <i class="fas fa-calendar-day"></i>
              <span class="date-group-label">{{ group.label }}</span>
              <span class="date-group-count">{{ group.items.length }} 篇</span>
            </div>
            <article
              v-for="item in group.items"
              :key="item.id"
              class="article-card"
              @click="openDetail(item)"
            >
              <div class="card-left">
                <span class="source-badge" :class="sourceClass(item.source)">{{ item.source }}</span>
              </div>
              <div class="card-body">
                <h3 class="article-title">{{ item.title }}</h3>
                <p class="article-summary" v-if="item.summary">{{ truncateText(item.summary, 150) }}</p>
                <div class="article-meta">
                  <span class="meta-item" v-if="item.author"><i class="fas fa-user"></i> {{ item.author }}</span>
                  <span class="meta-item" v-if="item.publish_date"><i class="fas fa-clock"></i> {{ formatTime(item.publish_date) }}</span>
                  <span class="meta-item" v-if="item.category"><i class="fas fa-tag"></i> {{ item.category }}</span>
                  <span class="meta-item" v-if="item.region"><i class="fas fa-map-marker-alt"></i> {{ item.region }}</span>
                </div>
              </div>
              <div class="card-right">
                <button
                  v-if="authStore.isLoggedIn"
                  class="card-delete-btn"
                  title="删除"
                  @click.stop="handleDeleteArticle(item)"
                >
                  <i class="fas fa-times"></i>
                </button>
                <i class="fas fa-chevron-right"></i>
              </div>
            </article>
          </div>
        </div>

        <div v-if="total > pageSize" class="pagination">
          <button class="page-btn" :disabled="currentPage === 1" @click="changePage(-1)">
            <i class="fas fa-chevron-left"></i>
          </button>
          <span class="page-info">第 {{ currentPage }} 页 / 共 {{ totalPages }} 页 ({{ total }} 条)</span>
          <button class="page-btn" :disabled="currentPage === totalPages" @click="changePage(1)">
            <i class="fas fa-chevron-right"></i>
          </button>
        </div>
      </div>
    </div>

    <transition name="modal">
      <div v-if="selectedArticle" class="modal-overlay" @click.self="closeDetail">
        <div class="modal-container">
          <button class="modal-close" @click="closeDetail"><i class="fas fa-times"></i></button>

          <div class="modal-content">
            <div class="modal-header">
              <span class="source-badge" :class="sourceClass(selectedArticle.source)">{{ selectedArticle.source }}</span>
              <span class="modal-date" v-if="selectedArticle.publish_date">{{ formatDate(selectedArticle.publish_date) }}</span>
            </div>
            <h2 class="modal-title">{{ selectedArticle.title }}</h2>

            <div class="modal-info-bar">
              <span class="info-item" v-if="selectedArticle.author"><i class="fas fa-user"></i> {{ selectedArticle.author }}</span>
              <span class="info-item" v-if="selectedArticle.category"><i class="fas fa-tag"></i> {{ selectedArticle.category }}</span>
              <span class="info-item" v-if="selectedArticle.region"><i class="fas fa-map-marker-alt"></i> {{ selectedArticle.region }}</span>
              <span class="info-item"><i class="fas fa-clock"></i> 采集于 {{ formatDate(selectedArticle.crawl_date) }}</span>
            </div>

            <div class="modal-text" v-if="selectedArticle.content">
              <p v-for="(para, i) in contentParagraphs" :key="i">{{ para }}</p>
            </div>
            <div v-else class="modal-text-empty">暂无正文内容</div>

            <div class="modal-footer" v-if="selectedArticle.source_url">
              <a :href="selectedArticle.source_url" target="_blank" class="source-link">
                <i class="fas fa-external-link-alt"></i> 查看原文
              </a>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <AppFooter />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import { useAuthStore } from '@/stores/auth'
import { listArticles, listTodayArticles, getSources, triggerCrawl, deleteArticle, clearAllArticles } from '@/api/crawler'

const authStore = useAuthStore()

const loading = ref(true)
const crawling = ref(false)
const clearing = ref(false)
const articles = ref([])
const total = ref(0)
const totalPages = ref(1)
const currentPage = ref(1)
const pageSize = 20
const searchKeyword = ref('')
const filterSource = ref('')
const filterDateStart = ref('')
const filterDateEnd = ref('')
const sources = ref([])
const selectedArticle = ref(null)
const todayArticles = ref([])
const todayLoading = ref(false)

const todayLabel = computed(() => {
  const d = new Date()
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
})

const contentParagraphs = computed(() => {
  if (!selectedArticle.value?.content) return []
  return selectedArticle.value.content.split('\n').filter(p => p.trim())
})

const groupedArticles = computed(() => {
  const groups = {}
  for (const item of articles.value) {
    const dateStr = item.publish_date ? formatDate(item.publish_date) : '未知日期'
    if (!groups[dateStr]) {
      groups[dateStr] = { key: dateStr, label: formatDateLabel(item.publish_date), items: [] }
    }
    groups[dateStr].items.push(item)
  }
  return Object.values(groups).sort((a, b) => {
    if (a.key === '未知日期') return 1
    if (b.key === '未知日期') return -1
    return b.key.localeCompare(a.key)
  })
})

function truncateText(text, max) {
  if (!text) return ''
  if (text.length <= max) return text
  return text.substring(0, max) + '...'
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

function formatDateLabel(dateStr) {
  if (!dateStr) return '未知日期'
  const d = new Date(dateStr)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const itemDate = new Date(d.getFullYear(), d.getMonth(), d.getDate())
  const diff = Math.round((today - itemDate) / 86400000)
  const base = `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`
  if (diff === 0) return `今天 (${base})`
  if (diff === 1) return `昨天 (${base})`
  if (diff === 2) return `前天 (${base})`
  return base
}

function formatTime(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  const time = `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
  const date = formatDate(dateStr)
  return `${date} ${time}`
}

function sourceClass(source) {
  if (!source) return ''
  if (source.includes('民政')) return 'badge-mca'
  if (source.includes('新华')) return 'badge-xinhua'
  if (source.includes('新疆')) return 'badge-xinjiang'
  if (source.includes('民委')) return 'badge-neac'
  if (source.includes('发改')) return 'badge-ndrc'
  if (source.includes('工信')) return 'badge-miit'
  if (source.includes('政府网')) return 'badge-gov'
  if (source.includes('边疆')) return 'badge-bjs'
  return ''
}

async function loadTodayArticles() {
  todayLoading.value = true
  try {
    const result = await listTodayArticles({ page: 1, page_size: 50 })
    todayArticles.value = result.items || []
  } catch {
    todayArticles.value = []
  } finally {
    todayLoading.value = false
  }
}

async function loadData() {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize
    }
    if (filterSource.value) params.source = filterSource.value
    if (searchKeyword.value.trim()) params.keyword = searchKeyword.value.trim()
    if (filterDateStart.value) params.start_date = filterDateStart.value
    if (filterDateEnd.value) params.end_date = filterDateEnd.value

    const result = await listArticles(params)
    articles.value = result.items || []
    total.value = result.total || 0
    totalPages.value = result.total_pages || 1
  } catch (e) {
    console.error('加载资讯失败:', e)
    ElMessage.error('加载资讯失败')
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  currentPage.value = 1
  loadData()
}

function changePage(delta) {
  const next = currentPage.value + delta
  if (next >= 1 && next <= totalPages.value) {
    currentPage.value = next
    loadData()
    window.scrollTo({ top: 300, behavior: 'smooth' })
  }
}

async function openDetail(item) {
  try {
    const detail = await listArticles({
      page: 1,
      page_size: 1,
      keyword: item.title.substring(0, 10)
    })
    if (detail.items && detail.items.length > 0) {
      selectedArticle.value = detail.items[0]
    } else {
      selectedArticle.value = item
    }
    document.body.style.overflow = 'hidden'
  } catch {
    selectedArticle.value = item
    document.body.style.overflow = 'hidden'
  }
}

function closeDetail() {
  selectedArticle.value = null
  document.body.style.overflow = ''
}

async function handleTrigger() {
  crawling.value = true
  try {
    const result = await triggerCrawl(filterSource.value || undefined)
    ElMessage.success(result.message)
    if (result.crawled > 0) {
      currentPage.value = 1
      await Promise.all([loadData(), loadTodayArticles()])
    }
    if (result.errors && result.errors.length > 0) {
      ElMessage.warning(`部分错误: ${result.errors.length} 条`)
    }
  } catch (e) {
    const msg = e.response?.data?.detail || '采集失败，请稍后重试'
    ElMessage.error(msg)
  } finally {
    crawling.value = false
  }
}

onMounted(async () => {
  try {
    const data = await getSources()
    sources.value = data.sources || []
  } catch {
    // Sources endpoint may fail, non-critical
  }
  await Promise.all([loadData(), loadTodayArticles()])
})

async function handleDeleteArticle(article) {
  if (!confirm(`确认删除这篇文章？\n${article.title}`)) return
  try {
    await deleteArticle(article.id)
    ElMessage.success('已删除')
    if (articles.value.length === 1 && currentPage.value > 1) {
      currentPage.value--
    }
    await loadData()
  } catch (e) {
    const msg = e.response?.data?.detail || '删除失败'
    ElMessage.error(msg)
  }
}

async function handleClearAll() {
  const target = filterSource.value
    ? sources.value.find(s => s.key === filterSource.value)?.name || '当前信源'
    : '全部'
  if (!confirm(`确认清空${target}的文章数据？此操作不可恢复！`)) return
  clearing.value = true
  try {
    const result = await clearAllArticles(filterSource.value || undefined)
    ElMessage.success(result.message)
    currentPage.value = 1
    await loadData()
  } catch (e) {
    const msg = e.response?.data?.detail || '清空失败'
    ElMessage.error(msg)
  } finally {
    clearing.value = false
  }
}
</script>

<style scoped>
.crawler-page {
  min-height: 100vh;
}

.page-banner {
  background: linear-gradient(135deg, #2c3e50 0%, #3498db 50%, #2c3e50 100%);
  color: white;
  padding: 50px 5% 35px;
  text-align: center;
}

.banner-content {
  max-width: 800px;
  margin: 0 auto;
}

.page-banner h1 {
  font-size: 2.5rem;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.page-banner p {
  font-size: 1.1rem;
  opacity: 0.9;
}

.content-wrapper {
  max-width: 1000px;
  margin: 0 auto;
  padding: 25px 20px;
}

.toolbar {
  display: flex;
  gap: 10px;
  margin-bottom: 25px;
  flex-wrap: wrap;
  align-items: center;
}

.search-box {
  flex: 1;
  min-width: 200px;
  position: relative;
}

.search-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
}

.search-input {
  width: 100%;
  padding: 11px 16px 11px 40px;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 0.95rem;
  transition: border-color 0.3s;
}

.search-input:focus {
  border-color: #3498db;
  outline: none;
}

.filter-select,
.date-input {
  padding: 11px 14px;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 0.9rem;
  background: white;
  cursor: pointer;
}

.filter-select:focus,
.date-input:focus {
  border-color: #3498db;
  outline: none;
}

.date-sep {
  color: #999;
  font-size: 0.9rem;
}

.trigger-btn {
  padding: 11px 20px;
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
}

.trigger-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4);
}

.trigger-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.clear-btn {
  padding: 11px 20px;
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
}

.clear-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(231, 76, 60, 0.4);
}

.clear-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.today-section {
  margin-bottom: 30px;
  background: linear-gradient(135deg, #eef6ff, #f0f7ff);
  border-radius: 14px;
  padding: 20px;
  border: 1px solid #d0e3f7;
}

.today-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.today-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.2rem;
  font-weight: 700;
  color: #1a5276;
}

.today-title i {
  color: #f39c12;
  font-size: 1.3rem;
}

.today-date {
  font-size: 0.85rem;
  font-weight: 400;
  color: #7f8c8d;
}

.today-count {
  font-size: 0.85rem;
  color: #2980b9;
  background: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-weight: 600;
}

.today-scroll {
  display: flex;
  gap: 14px;
  overflow-x: auto;
  padding-bottom: 10px;
  scroll-behavior: smooth;
}

.today-scroll::-webkit-scrollbar {
  height: 6px;
}

.today-scroll::-webkit-scrollbar-track {
  background: #e8eef5;
  border-radius: 3px;
}

.today-scroll::-webkit-scrollbar-thumb {
  background: #b0c4de;
  border-radius: 3px;
}

.today-card {
  flex: 0 0 280px;
  background: white;
  border-radius: 12px;
  padding: 16px;
  cursor: pointer;
  transition: transform 0.25s, box-shadow 0.25s;
  border: 1px solid #e8eef5;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.today-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(52, 152, 219, 0.15);
}

.today-card-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #333;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.today-card-summary {
  font-size: 0.82rem;
  color: #666;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.today-card-time {
  font-size: 0.78rem;
  color: #999;
  display: flex;
  align-items: center;
  gap: 4px;
}

.loading {
  text-align: center;
  padding: 60px;
  color: #999;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.no-data {
  text-align: center;
  padding: 60px;
  color: #999;
}

.no-data-icon {
  font-size: 3rem;
  margin-bottom: 15px;
  color: #ddd;
}

.no-data-hint {
  font-size: 0.9rem;
  color: #aaa;
  margin-top: 8px;
}

.article-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.date-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.date-group-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: linear-gradient(135deg, #f0f4f8, #e8eef5);
  border-left: 4px solid #3498db;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 700;
  color: #2c3e50;
  position: sticky;
  top: 0;
  z-index: 10;
}

.date-group-header i {
  color: #3498db;
}

.date-group-label {
  flex: 1;
}

.date-group-count {
  font-size: 0.8rem;
  font-weight: 500;
  color: #7f8c8d;
  background: white;
  padding: 2px 10px;
  border-radius: 10px;
}

.article-card {
  display: flex;
  align-items: stretch;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.06);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  border: 1px solid #f0f0f0;
}

.article-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.card-left {
  width: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  flex-shrink: 0;
}

.source-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 700;
  background: #e0e0e0;
  color: #555;
  text-align: center;
  white-space: nowrap;
}

.badge-mca {
  background: #e8f5e9;
  color: #2e7d32;
}

.badge-xinhua {
  background: #ffebee;
  color: #c62828;
}

.badge-xinjiang {
  background: #e3f2fd;
  color: #1565c0;
}

.badge-neac {
  background: #f3e5f5;
  color: #7b1fa2;
}

.badge-ndrc {
  background: #fff3e0;
  color: #e65100;
}

.badge-miit {
  background: #e0f7fa;
  color: #006064;
}

.badge-gov {
  background: #fce4ec;
  color: #880e4f;
}

.badge-bjs {
  background: #e8eaf6;
  color: #283593;
}

.card-body {
  flex: 1;
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.article-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 6px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-summary {
  font-size: 0.88rem;
  color: #666;
  line-height: 1.5;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-meta {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.meta-item {
  font-size: 0.8rem;
  color: #888;
  display: flex;
  align-items: center;
  gap: 4px;
}

.card-right {
  display: flex;
  align-items: center;
  padding: 0 18px;
  color: #ccc;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.article-card:hover .card-right {
  color: #3498db;
}

.card-delete-btn {
  width: 28px;
  height: 28px;
  border: none;
  background: transparent;
  color: #ccc;
  border-radius: 50%;
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-delete-btn:hover {
  background: #e74c3c;
  color: white;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-top: 30px;
}

.page-btn {
  padding: 10px 18px;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.page-btn:hover:not(:disabled) {
  border-color: #3498db;
  color: #3498db;
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-info {
  color: #666;
  font-size: 0.9rem;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  overflow-y: auto;
}

.modal-container {
  background: white;
  border-radius: 16px;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  padding: 35px;
}

.modal-close {
  position: absolute;
  top: 15px;
  right: 15px;
  width: 36px;
  height: 36px;
  border: none;
  background: #f5f5f5;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.1rem;
  color: #666;
  transition: all 0.3s;
  z-index: 1;
}

.modal-close:hover {
  background: #e74c3c;
  color: white;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.modal-date {
  font-size: 0.85rem;
  color: #999;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 15px;
  line-height: 1.4;
}

.modal-info-bar {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
  padding: 12px 0;
  border-top: 1px solid #f0f0f0;
  border-bottom: 1px solid #f0f0f0;
  margin-bottom: 20px;
}

.info-item {
  font-size: 0.85rem;
  color: #777;
  display: flex;
  align-items: center;
  gap: 5px;
}

.modal-text {
  font-size: 0.95rem;
  color: #444;
  line-height: 1.8;
  margin-bottom: 20px;
}

.modal-text p {
  margin-bottom: 12px;
}

.modal-text-empty {
  text-align: center;
  padding: 40px;
  color: #ccc;
  font-size: 1.1rem;
}

.modal-footer {
  padding-top: 15px;
  border-top: 1px solid #f0f0f0;
}

.source-link {
  color: #3498db;
  font-size: 0.9rem;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  transition: color 0.3s;
}

.source-link:hover {
  color: #2980b9;
}

/* Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.3s;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.95);
}

@media (max-width: 768px) {
  .page-banner h1 {
    font-size: 1.8rem;
  }

  .card-left {
    width: 70px;
  }

  .source-badge {
    font-size: 0.72rem;
    padding: 4px 8px;
  }

  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .date-sep {
    display: none;
  }

  .modal-container {
    padding: 20px;
  }
}
</style>
