<template>
  <div class="page">
    <AppHeader />

    <div class="achievement-page">
      <header class="page-banner">
        <div class="banner-content">
          <h1><i class="fas fa-trophy"></i> 成果展示</h1>
          <p>东西协作成果案例库</p>
          <div class="banner-stats">
            <div class="stat-item">
              <span class="stat-num">{{ achievements.length }}</span>
              <span class="stat-label">已完成成果</span>
            </div>
          </div>
        </div>
      </header>

      <div class="content-wrapper">
        <div class="toolbar">
          <div class="search-box">
            <i class="fas fa-search search-icon"></i>
            <input
              v-model="searchKeyword"
              type="text"
              placeholder="搜索标题、地区、关键词..."
              class="search-input"
            />
          </div>
          <select v-model="filterType" class="filter-select">
            <option value="">全部类型</option>
            <option v-for="t in achievementTypes" :key="t" :value="t">{{ t }}</option>
          </select>
        </div>

        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          <p>正在加载案例数据...</p>
        </div>

        <div v-else-if="filteredData.length === 0" class="no-data">
          <i class="fas fa-folder-open no-data-icon"></i>
          <p>未找到匹配的案例</p>
        </div>

        <!-- 已完成成果 -->
        <div v-else class="card-grid">
          <article
            v-for="item in pagedData"
            :key="item['成果ID']"
            class="case-card achievement-card"
            @click="openDetail(item, 'achievement')"
          >
            <div class="card-image" v-if="item.image">
              <img :src="item.image" :alt="item['成果标题']" loading="lazy" />
            </div>
            <div class="card-image card-image-placeholder" v-else>
              <i class="fas fa-image"></i>
            </div>
            <div class="card-body">
              <div class="card-tag">{{ item['成果类型'] || '综合' }}</div>
              <h3 class="card-title">{{ item['成果标题'] }}</h3>
              <div class="card-meta">
                <span class="meta-item"><i class="fas fa-map-marker-alt"></i> {{ truncateText(item['实施/合作地区'], 20) }}</span>
                <span class="meta-item"><i class="fas fa-calendar"></i> {{ item['完成时间'] || '待定' }}</span>
              </div>
              <p class="card-highlight">{{ truncateText(item['核心亮点与量化成效'], 100) }}</p>
              <div class="card-footer">
                <span class="card-id">{{ item['成果ID'] }}</span>
                <span class="view-detail">查看详情 <i class="fas fa-arrow-right"></i></span>
              </div>
            </div>
          </article>
        </div>

        <!-- Pagination -->
        <div v-if="filteredData.length > itemsPerPage" class="pagination">
          <button class="page-btn" :disabled="currentPage === 1" @click="changePage(-1)">
            <i class="fas fa-chevron-left"></i>
          </button>
          <span class="page-info">第 {{ currentPage }} 页 / 共 {{ totalPages }} 页 ({{ filteredData.length }} 条)</span>
          <button class="page-btn" :disabled="currentPage === totalPages" @click="changePage(1)">
            <i class="fas fa-chevron-right"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Detail Modal -->
    <transition name="modal">
      <div v-if="selectedItem" class="modal-overlay" @click.self="closeDetail">
        <div class="modal-container">
          <button class="modal-close" @click="closeDetail"><i class="fas fa-times"></i></button>

          <div v-if="detailType === 'achievement'" class="modal-content">
            <img v-if="selectedItem.image" :src="selectedItem.image" class="modal-image" :alt="selectedItem['成果标题']" />
            <h2 class="modal-title">{{ selectedItem['成果标题'] }}</h2>
            <div class="modal-tags">
              <span class="modal-tag">{{ selectedItem['成果类型'] }}</span>
              <span class="modal-tag">{{ selectedItem['成果ID'] }}</span>
            </div>
            <div class="modal-grid">
              <div class="modal-field"><label>实施/合作地区</label><p>{{ selectedItem['实施/合作地区'] }}</p></div>
              <div class="modal-field"><label>合作双方/实施主体</label><p>{{ selectedItem['合作双方/实施主体'] }}</p></div>
              <div class="modal-field"><label>完成时间</label><p>{{ selectedItem['完成时间'] }}</p></div>
              <div class="modal-field"><label>成果类型</label><p>{{ selectedItem['成果类型'] }}</p></div>
            </div>
            <div class="modal-section"><h4>完成的工作/任务</h4><p>{{ selectedItem['完成的工作/任务'] }}</p></div>
            <div class="modal-section"><h4>核心亮点与量化成效</h4><p>{{ selectedItem['核心亮点与量化成效'] }}</p></div>
            <div class="modal-section"><h4>可复制协作点</h4><p>{{ selectedItem['可复制协作点'] }}</p></div>
            <div class="modal-section" v-if="selectedItem['原文链接']">
              <h4>原文链接</h4>
              <a :href="selectedItem['原文链接']" target="_blank" class="source-link">{{ selectedItem['原文链接'] }}</a>
            </div>
          </div>

          <div v-else class="modal-content">
            <p>未知类型</p>
          </div>
        </div>
      </div>
    </transition>

    <AppFooter />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'

const loading = ref(true)
const searchKeyword = ref('')
const currentPage = ref(1)
const itemsPerPage = 9

const achievements = ref([])
const filterType = ref('')

const selectedItem = ref(null)
const detailType = ref('')

const achievementTypes = computed(() => {
  const types = new Set()
  achievements.value.forEach(a => {
    if (a['成果类型']) types.add(a['成果类型'])
  })
  return Array.from(types).sort()
})

const filteredData = computed(() => {
  let data = achievements.value

  const kw = searchKeyword.value.trim().toLowerCase()
  if (kw) {
    data = data.filter(item => {
      return Object.values(item).some(v =>
        String(v).toLowerCase().includes(kw)
      )
    })
  }

  if (filterType.value) {
    data = data.filter(a => a['成果类型'] === filterType.value)
  }

  return data
})

const totalPages = computed(() => Math.ceil(filteredData.value.length / itemsPerPage))

const pagedData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return filteredData.value.slice(start, start + itemsPerPage)
})

function truncateText(text, max) {
  if (!text) return ''
  if (text.length <= max) return text
  return text.substring(0, max) + '...'
}

function changePage(delta) {
  const next = currentPage.value + delta
  if (next >= 1 && next <= totalPages.value) {
    currentPage.value = next
    window.scrollTo({ top: 400, behavior: 'smooth' })
  }
}

function openDetail(item, type) {
  selectedItem.value = item
  detailType.value = type
  document.body.style.overflow = 'hidden'
}

function closeDetail() {
  selectedItem.value = null
  document.body.style.overflow = ''
}

watch([searchKeyword, filterType], () => {
  currentPage.value = 1
})

onMounted(async () => {
  try {
    const res = await fetch('/data/achievements.json')
    const data = await res.json()
    achievements.value = data.achievements || []
  } catch (e) {
    console.error('加载案例数据失败:', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.achievement-page {
  min-height: 100vh;
}

.page-banner {
  background: linear-gradient(135deg, #c0392b 0%, #e74c3c 50%, #c0392b 100%);
  color: white;
  padding: 60px 5% 40px;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.page-banner::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60"><circle cx="30" cy="30" r="1" fill="rgba(255,255,255,0.15)"/></svg>');
}

.banner-content {
  position: relative;
  z-index: 1;
  max-width: 900px;
  margin: 0 auto;
}

.page-banner h1 {
  font-size: 2.8rem;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.page-banner p {
  font-size: 1.2rem;
  opacity: 0.9;
  margin-bottom: 25px;
}

.banner-stats {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 30px;
  margin-top: 20px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-num {
  font-size: 2.2rem;
  font-weight: 800;
}

.stat-label {
  font-size: 0.95rem;
  opacity: 0.85;
}

.stat-divider {
  width: 1px;
  height: 40px;
  background: rgba(255, 255, 255, 0.3);
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 20px;
}

.tab-bar {
  display: flex;
  gap: 5px;
  margin-bottom: 20px;
  background: #f5f5f5;
  border-radius: 12px;
  padding: 6px;
}

.tab-btn {
  flex: 1;
  padding: 14px 20px;
  border: none;
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  color: #666;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.tab-btn.active {
  background: white;
  color: #c0392b;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

.tab-count {
  background: #e74c3c22;
  color: #c0392b;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.8rem;
}

.tab-btn.active .tab-count {
  background: #c0392b;
  color: white;
}

.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 25px;
  flex-wrap: wrap;
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
  padding: 12px 16px 12px 42px;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.search-input:focus {
  border-color: #e74c3c;
  outline: none;
}

.filter-select {
  padding: 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 1rem;
  background: white;
  cursor: pointer;
  min-width: 140px;
}

.filter-select:focus {
  border-color: #e74c3c;
  outline: none;
}

.loading {
  text-align: center;
  padding: 60px;
  color: #999;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #c0392b;
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

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 25px;
}

.card-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.case-card {
  background: white;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  border: 1px solid #f0f0f0;
}

.case-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
}

.achievement-card {
  display: flex;
  flex-direction: column;
}

.card-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
  position: relative;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s;
}

.case-card:hover .card-image img {
  transform: scale(1.05);
}

.card-image-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  color: #ccc;
  font-size: 2rem;
}

.card-body {
  padding: 18px 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card-tag {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 0.78rem;
  font-weight: 600;
  background: #e74c3c22;
  color: #c0392b;
  margin-bottom: 8px;
  align-self: flex-start;
}

.tag-demand {
  background: #2980b922;
  color: #2980b9;
}

.tag-supply {
  background: #27ae6022;
  color: #27ae60;
}

.card-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.card-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 10px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  gap: 15px;
  margin-bottom: 10px;
  flex-wrap: wrap;
}

.meta-item {
  font-size: 0.85rem;
  color: #777;
  display: flex;
  align-items: center;
  gap: 5px;
}

.card-highlight {
  font-size: 0.9rem;
  color: #555;
  line-height: 1.6;
  margin-bottom: 10px;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-sub {
  font-size: 0.85rem;
  color: #888;
  line-height: 1.5;
  margin-bottom: 10px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
  border-top: 1px solid #f0f0f0;
}

.card-id {
  font-size: 0.8rem;
  color: #aaa;
  font-weight: 500;
}

.view-detail {
  font-size: 0.85rem;
  color: #c0392b;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: gap 0.3s;
}

.case-card:hover .view-detail {
  gap: 8px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-top: 35px;
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
  border-color: #c0392b;
  color: #c0392b;
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

.modal-image {
  width: 100%;
  max-height: 350px;
  object-fit: cover;
  border-radius: 12px;
  margin-bottom: 20px;
}

.modal-title {
  font-size: 1.6rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 12px;
  line-height: 1.4;
}

.modal-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}

.modal-tag {
  padding: 4px 12px;
  border-radius: 14px;
  font-size: 0.82rem;
  font-weight: 600;
  background: #e74c3c22;
  color: #c0392b;
}

.modal-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-bottom: 20px;
}

.modal-field label {
  font-size: 0.82rem;
  color: #999;
  font-weight: 600;
  display: block;
  margin-bottom: 4px;
}

.modal-field p {
  font-size: 0.95rem;
  color: #333;
  line-height: 1.5;
}

.modal-section {
  margin-bottom: 18px;
}

.modal-section h4 {
  font-size: 1rem;
  font-weight: 700;
  color: #c0392b;
  margin-bottom: 6px;
  padding-bottom: 4px;
  border-bottom: 2px solid #e74c3c33;
}

.modal-section p {
  font-size: 0.92rem;
  color: #444;
  line-height: 1.7;
}

.source-link {
  color: #3498db;
  font-size: 0.88rem;
  word-break: break-all;
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
    font-size: 2rem;
  }

  .banner-stats {
    gap: 15px;
  }

  .stat-num {
    font-size: 1.6rem;
  }

  .card-grid {
    grid-template-columns: 1fr;
  }

  .tab-btn {
    padding: 10px 12px;
    font-size: 0.85rem;
  }

  .toolbar {
    flex-direction: column;
  }

  .modal-grid {
    grid-template-columns: 1fr;
  }

  .modal-container {
    padding: 20px;
  }
}
</style>
