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


      <!-- 实践纪实 · 团队图集（真实调研素材） -->
      <section class="fieldwork">
        <div class="fw-head">
          <p class="fw-kicker">实践纪实 · 万里边疆 强国有我</p>
          <h2 class="fw-title">山东大学赴边疆社会实践图集</h2>
          <p class="fw-lede">以下 {{ fieldworkTotal }} 张照片均为实践团队真实调研影像，按主题归档——从"万里边疆 强国有我"启动授旗，到赴疆推普、支教课堂、医疗义诊与产业一线，图文一一对应。</p>
        </div>
        <div v-for="g in fieldworkGroups" :key="g.theme" class="fw-group">
          <h3 class="fw-group-h">{{ g.theme }}<span class="fw-count">{{ g.items.length }}</span></h3>
          <div class="fw-grid">
            <figure v-for="it in g.items" :key="it.src" class="fw-item" @click="openPhoto(it)">
              <img :src="it.src" :alt="it.caption" loading="lazy" />
              <figcaption class="fw-cap">{{ it.caption }}</figcaption>
            </figure>
          </div>
        </div>
      </section>

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


    <!-- Photo Lightbox -->
    <transition name="modal">
      <div v-if="photo" class="photo-overlay" @click.self="photo = null">
        <button class="modal-close photo-close" @click="photo = null"><i class="fas fa-times"></i></button>
        <figure class="photo-body">
          <img :src="photo.src" :alt="photo.caption" />
          <figcaption><span class="photo-theme">{{ photo.theme }}</span>{{ photo.caption }}</figcaption>
        </figure>
      </div>
    </transition>

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

/* ---------- 实践纪实图集（真实调研素材，按主题归档；2026-08-27 全部经读图逐张核对） ---------- */
const A = '/img/achievements'
const fieldworkGroups = [
  {
    theme: '项目启动',
    items: [
      { src: `${A}/图片16.png`, theme: '项目启动', caption: '「万里边疆 强国有我」社会实践育人工程启动会议（2025年7月8日），山东大学边疆研究院部署年度赴边疆实践；云南研究院授旗，「滇忆云桥」中队出征' },
    ],
  },
  {
    theme: '研究院团队纪实',
    items: [
      { src: `${A}/图片5.png`, theme: '团队纪实', caption: '山东大学「豪外听鸿」赴边疆研究院征实践团队在「为天下储人才，为国家图富强」校训墙前整装出征' },
      { src: `${A}/图片2.png`, theme: '思政育人', caption: '「万里边疆 青春强国行」多线并进：经济学院「疆山河」中队赴和田、兵团团场学习传承兵团精神，并在疏附县托克扎克镇中心小学开展思政育人调研' },
    ],
  },
  {
    theme: '赴疆调研 · 铸牢共同体',
    items: [
      { src: `${A}/图片3.png`, theme: '生态兴边', caption: '「疆山河行」赴边疆生态兴边调研实践团在伊犁特克斯县库什台村，与村党支部围绕生态保护与兴边富民座谈' },
      { src: `${A}/图片8.png`, theme: '民族团结', caption: '铸牢中华民族共同体意识实践团在兵团第六师奇台农场民族团结教育基地，学习「中华民族一家亲，同心共筑中国梦」主题展陈' },
      { src: `${A}/图片14.png`, theme: '屯垦戍边', caption: '青鸾海疆实践队在奇台民兵连纪念碑前，访谈军垦后代、记录民兵连屯垦戍边口述史' },
    ],
  },
  {
    theme: '推普强国',
    items: [
      { src: `${A}/图片1.png`, theme: '推普强国', caption: '推普强国行实践队在喀什中亚南亚工业园党群服务中心，开展「普通话+就业场景」语言服务调研（对应成果档案条目53）' },
      { src: `${A}/图片18.png`, theme: '推普课堂', caption: '推普课堂上，孩子们展示毛笔书写的国家通用语言文字——「各民族要像石榴籽一样紧紧抱在一起」' },
    ],
  },
  {
    theme: '教育帮扶与支教',
    items: [
      { src: `${A}/图片10.png`, theme: '技能培训调研', caption: '在疏附县技工学校座谈（「知识改变命运、技能成就未来」），调研职业技能培训与国家通用语言文字推广' },
      { src: `${A}/图片12.png`, theme: '支教课堂', caption: '「华夏彩课堂」中华优秀传统文化进校园：漆扇书签、绒花制作、经典诵读、纸艺拼贴等九大课程板块' },
      { src: `${A}/图片11.png`, theme: '教研交流', caption: '中华优秀传统文化进课堂与教研交流：实践团与当地教师围绕课程设计联合备课' },
    ],
  },
  {
    theme: '产业与科技调研',
    items: [
      { src: `${A}/图片17.png`, theme: '产业调研', caption: '产业一线走访：生物发酵车间、洁净生产间、智能展示厅与工业设备区，记录东西部协作产业园的技术转化场景' },
      { src: `${A}/图片15.png`, theme: '科技兴农', caption: '农林植保无人机与农机装备调研，了解智能装备在边疆特色农业中的应用' },
      { src: `${A}/图片7.png`, theme: '基建能源', caption: '山东大学通麦驻地：实践团在川藏交通与能源建设一线，调研重大工程建设与运维' },
      { src: `${A}/图片4.png`, theme: '规划调研', caption: '在城市规划馆聆听讲解，系统了解受援地发展脉络与对口支援项目布局' },
    ],
  },
  {
    theme: '医疗义诊',
    items: [
      { src: `${A}/图片6.png`, theme: '医疗义诊', caption: '山东大学齐鲁医院硕博医师团边疆义诊现场，专家为群众提供基层医疗服务' },
    ],
  },
  {
    theme: '文化交融',
    items: [
      { src: `${A}/图片13.png`, theme: '文化调研', caption: '暖城新声社会实践队在鄂尔多斯青铜器博物馆，调研北疆文化保护与传播' },
      { src: `${A}/图片9.png`, theme: '高原调研', caption: '山东大学药学院蓉城同道实践团赴西藏，开展高原医药与健康调研' },
      { src: `${A}/图片19.png`, theme: '座谈交流', caption: '实践团与当地政府部门、园区企业多场座谈（中新社山东报道）' },
    ],
  },
]
const fieldworkTotal = fieldworkGroups.reduce((n, g) => n + g.items.length, 0)
const photo = ref(null)
const openPhoto = (it) => { photo.value = it }

</script>

<style scoped>
.achievement-page {
  min-height: 100vh;
}

.page-banner {
  background: linear-gradient(135deg, var(--color-accent) 0%, var(--color-accent) 50%, var(--color-accent) 100%);
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
  color: var(--color-accent);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

.tab-count {
  background: var(--color-accent)22;
  color: var(--color-accent);
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.8rem;
}

.tab-btn.active .tab-count {
  background: var(--color-accent);
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
  border-color: var(--color-accent);
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
  border-color: var(--color-accent);
  outline: none;
}

.loading {
  text-align: center;
  padding: 60px;
  color: #999;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid var(--color-accent);
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
  background: linear-gradient(135deg, var(--paper-2), #e9ecef);
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
  background: var(--color-accent)22;
  color: var(--color-accent);
  margin-bottom: 8px;
  align-self: flex-start;
}

.tag-demand {
  background: var(--color-primary)22;
  color: var(--color-primary);
}

.tag-supply {
  background: var(--el-color-success)22;
  color: var(--el-color-success);
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
  color: var(--color-accent);
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
  border-color: var(--color-accent);
  color: var(--color-accent);
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
  background: var(--color-accent);
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
  background: var(--color-accent)22;
  color: var(--color-accent);
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
  color: var(--color-accent);
  margin-bottom: 6px;
  padding-bottom: 4px;
  border-bottom: 2px solid var(--color-accent)33;
}

.modal-section p {
  font-size: 0.92rem;
  color: #444;
  line-height: 1.7;
}

.source-link {
  color: var(--color-primary);
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

<style scoped>
/* ===== 实践纪实 · 编辑风图集 ===== */
.fieldwork {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 46px 4% 8px;
  border-bottom: 1px solid var(--rule);
}
.fw-kicker {
  font-size: 11px;
  letter-spacing: 3px;
  color: var(--color-accent);
  font-weight: 700;
  margin-bottom: 10px;
}
.fw-title {
  font-family: var(--font-serif);
  font-size: clamp(21px, 3vw, 27px);
  color: var(--ink);
  font-weight: 700;
  letter-spacing: 1px;
  margin-bottom: 10px;
}
.fw-lede {
  font-size: 13px;
  color: var(--ink-3);
  line-height: 1.9;
  max-width: 680px;
  margin-bottom: 30px;
}

.fw-group { margin-bottom: 30px; }
.fw-group-h {
  font-size: 13px;
  letter-spacing: 2.5px;
  color: var(--ink);
  font-weight: 650;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--rule);
  margin-bottom: 16px;
  display: flex;
  align-items: baseline;
  gap: 10px;
}
.fw-count {
  font-family: Georgia, var(--font-mono);
  font-size: 12px;
  color: var(--ink-3);
  font-weight: 400;
}

.fw-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 18px;
}
.fw-item {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
  cursor: zoom-in;
  transition: transform 0.3s var(--ease-out), box-shadow 0.3s var(--ease-out);
}
.fw-item:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}
.fw-item img {
  width: 100%;
  height: 170px;
  object-fit: cover;
  display: block;
}
.fw-cap {
  padding: 10px 12px 12px;
  font-size: 12px;
  line-height: 1.7;
  color: var(--ink-2);
  border-top: 1px solid var(--color-border);
}

/* 灯箱 */
.photo-overlay {
  position: fixed; inset: 0; z-index: 200;
  background: rgba(20, 18, 15, 0.88);
  display: flex; align-items: center; justify-content: center;
  padding: 40px 24px;
}
.photo-close { position: absolute; top: 22px; right: 26px; color: #fff; background: none; border: none; font-size: 20px; cursor: pointer; }
.photo-body { max-width: min(920px, 92vw); }
.photo-body img {
  max-width: 100%; max-height: 74vh;
  border-radius: var(--radius-sm);
  box-shadow: 0 24px 60px rgba(0,0,0,.5);
}
.photo-body figcaption {
  margin-top: 14px;
  font-size: 13px;
  line-height: 1.8;
  color: rgba(255,255,255,.88);
}
.photo-theme {
  display: inline-block;
  font-size: 11px;
  letter-spacing: 2px;
  color: #e8d9b8;
  border: 1px solid rgba(232,217,184,.4);
  border-radius: 2px;
  padding: 1px 8px;
  margin-right: 10px;
  vertical-align: 1px;
}
</style>
