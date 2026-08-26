<template>
  <div class="page">
    <AppHeader />

    <section class="page-header">
      <div class="container">
        <h1>
          <i class="fas fa-bullhorn"></i> 需求大厅
        </h1>
        <p>浏览边疆需求与内地供给信息，精准匹配东西协作合作方向</p>
      </div>
    </section>

    <div class="container content-area">
      <!-- Tab 栏 -->
      <div class="tab-bar">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          class="tab-btn"
          :class="{ active: activeTab === tab.key }"
          @click="switchTab(tab.key)"
        >
          <i :class="tab.icon"></i>
          {{ tab.label }}
          <span class="tab-count">{{ tab.count }}</span>
        </button>
      </div>

      <!-- ========== 边疆需求侧 ========== -->
      <template v-if="activeTab === 'borderDemands'">
        <div class="filter-container">
          <div class="filter-title">
            <i class="fas fa-filter"></i> 按省份筛选
          </div>
          <div class="category-filter">
            <button
              v-for="cat in borderCategories"
              :key="cat"
              class="category-btn"
              :class="{ active: selectedBdCategory === cat }"
              @click="selectBdCategory(cat)"
            >{{ cat }}</button>
          </div>
        </div>

        <div v-if="filteredBorderDemands.length > 0" class="results-info">
          <span>找到 <strong>{{ filteredBorderDemands.length }}</strong> 条边疆需求</span>
          <span>显示第 {{ bdDisplayRange }}</span>
        </div>

        <div v-if="filteredBorderDemands.length === 0" class="no-data">
          <i class="fas fa-folder-open no-data-icon"></i>
          <p>未找到匹配的边疆需求</p>
        </div>

        <main v-else class="demands-container">
          <article
            v-for="(item, index) in pagedBorderDemands"
            :key="item['需求ID']"
            class="demand-card border-demand-card"
          >
            <h2 class="demand-title">
              {{ item['需求标题'] }}
              <span class="status-tag bd-stage-tag">{{ item['需求阶段'] || '待定' }}</span>
              <span class="card-id">{{ item['需求ID'] }}</span>
            </h2>

            <div class="demand-info">
              <div class="info-item"><i class="fas fa-map-marker-alt"></i> {{ item['省/自治区'] || '未知' }}</div>
              <div class="info-item" v-if="item['地市/边境县/乡镇']"><i class="fas fa-location-arrow"></i> {{ truncateText(item['地市/边境县/乡镇'], 25) }}</div>
              <div class="info-item"><i class="fas fa-building"></i> {{ truncateText(item['需求发布方'], 30) }}</div>
            </div>

            <div v-if="item['适配供给标签']" class="detail-block">
              <div class="detail-block-label"><i class="fas fa-tag"></i> 适配供给标签</div>
              <div class="detail-block-content">{{ item['适配供给标签'] }}</div>
            </div>

            <div v-if="item['痛点/现状']" class="detail-block">
              <div class="detail-block-label"><i class="fas fa-exclamation-circle"></i> 痛点/现状</div>
              <div class="detail-block-content">{{ truncateText(item['痛点/现状'], 200) }}</div>
            </div>

            <div v-if="item['具体需求描述']" class="detail-block">
              <div class="detail-block-label"><i class="fas fa-file-alt"></i> 具体需求描述</div>
              <div class="detail-block-content">{{ truncateText(item['具体需求描述'], 200) }}</div>
            </div>

            <div v-if="item['预期目标及合作方式']" class="detail-block">
              <div class="detail-block-label"><i class="fas fa-bullseye"></i> 预期目标及合作方式</div>
              <div class="detail-block-content">{{ truncateText(item['预期目标及合作方式'], 150) }}</div>
            </div>

            <div class="contact-info">
              <div class="contact-details">
                <span class="contact-name">{{ truncateText(item['需求发布方'], 25) }}</span>
                <div class="contact-tags">
                  <span class="contact-tag">{{ item['省/自治区'] || '未知' }}</span>
                  <span class="contact-tag">{{ item['需求阶段'] || '待定' }}</span>
                </div>
              </div>
              <div class="contact-btns">
                <button class="match-btn" @click="runMatchSupplies(item)">
                  <i class="fas fa-magic"></i> 智能匹配供给方
                </button>
                <button class="contact-btn" @click="openDetail(item, 'demand')">
                  <i class="fas fa-eye"></i> 查看详情
                </button>
              </div>
            </div>

            <hr v-if="index < pagedBorderDemands.length - 1" class="divider" />
          </article>
        </main>

        <div v-if="bdTotalPages > 1" class="pagination-container">
          <div class="pagination">
            <button class="page-btn" :class="{ disabled: bdPage === 1 }" @click="changeBdPage(-1)">
              <i class="fas fa-chevron-left"></i>
            </button>
            <span class="page-info">第 {{ bdPage }} 页 / 共 {{ bdTotalPages }} 页 ({{ filteredBorderDemands.length }} 条)</span>
            <button class="page-btn" :class="{ disabled: bdPage === bdTotalPages }" @click="changeBdPage(1)">
              <i class="fas fa-chevron-right"></i>
            </button>
          </div>
        </div>
      </template>

      <!-- ========== 内地供给侧 ========== -->
      <template v-if="activeTab === 'mainlandSupply'">
        <div class="filter-container">
          <div class="filter-title">
            <i class="fas fa-filter"></i> 按主体类型筛选
          </div>
          <div class="category-filter">
            <button
              v-for="cat in supplyCategories"
              :key="cat"
              class="category-btn supply-cat-btn"
              :class="{ active: selectedMsCategory === cat }"
              @click="selectMsCategory(cat)"
            >{{ cat }}</button>
          </div>
        </div>

        <div v-if="filteredMainlandSupply.length > 0" class="results-info">
          <span>找到 <strong>{{ filteredMainlandSupply.length }}</strong> 条供给信息</span>
          <span>显示第 {{ msDisplayRange }}</span>
        </div>

        <div v-if="filteredMainlandSupply.length === 0" class="no-data">
          <i class="fas fa-folder-open no-data-icon"></i>
          <p>未找到匹配的供给信息</p>
        </div>

        <main v-else class="demands-container">
          <article
            v-for="(item, index) in pagedMainlandSupply"
            :key="item['供给ID']"
            class="demand-card supply-demand-card"
          >
            <h2 class="demand-title">
              {{ truncateText(item['提供方'], 35) }}
              <span class="status-tag ms-type-tag">{{ item['主体类型'] || '未知' }}</span>
              <span class="card-id">{{ item['供给ID'] }}</span>
            </h2>

            <div class="demand-info">
              <div class="info-item"><i class="fas fa-map-marker-alt"></i> {{ item['所在地'] || '未知' }}</div>
              <div class="info-item" v-if="item['合作交付方式']"><i class="fas fa-handshake"></i> {{ truncateText(item['合作交付方式'], 25) }}</div>
            </div>

            <div v-if="item['可提供服务']" class="detail-block">
              <div class="detail-block-label"><i class="fas fa-concierge-bell"></i> 可提供服务</div>
              <div class="detail-block-content">{{ truncateText(item['可提供服务'], 200) }}</div>
            </div>

            <div v-if="item['核心技术优势']" class="detail-block">
              <div class="detail-block-label"><i class="fas fa-cogs"></i> 核心技术优势</div>
              <div class="detail-block-content">{{ truncateText(item['核心技术优势'], 150) }}</div>
            </div>

            <div v-if="item['应用场景与案例']" class="detail-block">
              <div class="detail-block-label"><i class="fas fa-lightbulb"></i> 应用场景与案例</div>
              <div class="detail-block-content">{{ truncateText(item['应用场景与案例'], 150) }}</div>
            </div>

            <div v-if="item['适配边疆需求']" class="detail-block">
              <div class="detail-block-label"><i class="fas fa-link"></i> 适配边疆需求</div>
              <div class="detail-block-content">{{ truncateText(item['适配边疆需求'], 150) }}</div>
            </div>

            <div class="contact-info">
              <div class="contact-details">
                <span class="contact-name">{{ truncateText(item['提供方'], 25) }}</span>
                <div class="contact-tags">
                  <span class="contact-tag">{{ item['所在地'] || '未知' }}</span>
                  <span class="contact-tag">{{ item['主体类型'] || '未知' }}</span>
                </div>
              </div>
              <div class="contact-btns">
                <button class="match-btn match-demand-btn" @click="runMatchDemands(item)">
                  <i class="fas fa-bullseye"></i> 智能匹配需求
                </button>
                <button class="contact-btn supply-contact-btn" @click="openDetail(item, 'supply')">
                  <i class="fas fa-eye"></i> 查看详情
                </button>
              </div>
            </div>

            <hr v-if="index < pagedMainlandSupply.length - 1" class="divider" />
          </article>
        </main>

        <div v-if="msTotalPages > 1" class="pagination-container">
          <div class="pagination">
            <button class="page-btn" :class="{ disabled: msPage === 1 }" @click="changeMsPage(-1)">
              <i class="fas fa-chevron-left"></i>
            </button>
            <span class="page-info">第 {{ msPage }} 页 / 共 {{ msTotalPages }} 页 ({{ filteredMainlandSupply.length }} 条)</span>
            <button class="page-btn" :class="{ disabled: msPage === msTotalPages }" @click="changeMsPage(1)">
              <i class="fas fa-chevron-right"></i>
            </button>
          </div>
        </div>
      </template>

      <!-- 详情弹窗 -->
      <transition name="modal">
        <div v-if="selectedItem" class="modal-overlay" @click.self="closeDetail">
          <div class="modal-container">
            <button class="modal-close" @click="closeDetail"><i class="fas fa-times"></i></button>

            <div v-if="detailType === 'demand'" class="modal-content">
              <h2 class="modal-title">{{ selectedItem['需求标题'] }}</h2>
              <div class="modal-tags">
                <span class="modal-tag" v-if="selectedItem['需求阶段']">{{ selectedItem['需求阶段'] }}</span>
                <span class="modal-tag">{{ selectedItem['需求ID'] }}</span>
              </div>
              <div class="modal-grid">
                <div class="modal-field"><label>省/自治区</label><p>{{ selectedItem['省/自治区'] || '未提供' }}</p></div>
                <div class="modal-field"><label>地市/边境县/乡镇</label><p>{{ selectedItem['地市/边境县/乡镇'] || '未提供' }}</p></div>
                <div class="modal-field"><label>需求发布方</label><p>{{ selectedItem['需求发布方'] || '未提供' }}</p></div>
                <div class="modal-field"><label>适配供给标签</label><p>{{ selectedItem['适配供给标签'] || '未提供' }}</p></div>
              </div>
              <div class="modal-section" v-if="selectedItem['痛点/现状']"><h4>痛点/现状</h4><p>{{ selectedItem['痛点/现状'] }}</p></div>
              <div class="modal-section" v-if="selectedItem['具体需求描述']"><h4>具体需求描述</h4><p>{{ selectedItem['具体需求描述'] }}</p></div>
              <div class="modal-section" v-if="selectedItem['预期目标及合作方式']"><h4>预期目标及合作方式</h4><p>{{ selectedItem['预期目标及合作方式'] }}</p></div>
              <div class="modal-section" v-if="selectedItem['原文链接']"><h4>原文链接</h4><a :href="selectedItem['原文链接']" target="_blank" class="source-link">{{ selectedItem['原文链接'] }}</a></div>
            </div>

            <div v-else-if="detailType === 'supply'" class="modal-content">
              <h2 class="modal-title">{{ selectedItem['提供方'] }}</h2>
              <div class="modal-tags">
                <span class="modal-tag" v-if="selectedItem['主体类型']">{{ selectedItem['主体类型'] }}</span>
                <span class="modal-tag">{{ selectedItem['供给ID'] }}</span>
              </div>
              <div class="modal-grid">
                <div class="modal-field"><label>所在地</label><p>{{ selectedItem['所在地'] || '未提供' }}</p></div>
                <div class="modal-field"><label>主体类型</label><p>{{ selectedItem['主体类型'] || '未提供' }}</p></div>
              </div>
              <div class="modal-section" v-if="selectedItem['可提供服务']"><h4>可提供服务</h4><p>{{ selectedItem['可提供服务'] }}</p></div>
              <div class="modal-section" v-if="selectedItem['核心技术优势']"><h4>核心技术优势</h4><p>{{ selectedItem['核心技术优势'] }}</p></div>
              <div class="modal-section" v-if="selectedItem['应用场景与案例']"><h4>应用场景与案例</h4><p>{{ selectedItem['应用场景与案例'] }}</p></div>
              <div class="modal-section" v-if="selectedItem['适配边疆需求']"><h4>适配边疆需求</h4><p>{{ selectedItem['适配边疆需求'] }}</p></div>
              <div class="modal-section" v-if="selectedItem['合作交付方式']"><h4>合作交付方式</h4><p>{{ selectedItem['合作交付方式'] }}</p></div>
              <div class="modal-section" v-if="selectedItem['官网/案例链接']"><h4>官网/案例链接</h4><a :href="selectedItem['官网/案例链接']" target="_blank" class="source-link">{{ selectedItem['官网/案例链接'] }}</a></div>
            </div>
          </div>
        </div>
      </transition>

      <!-- 智能匹配弹窗 -->
      <transition name="modal">
        <div v-if="matchingLoading || matchingResult" class="modal-overlay" @click.self="closeMatching">
          <div class="modal-container matching-modal">
            <button class="modal-close" @click="closeMatching"><i class="fas fa-times"></i></button>

            <!-- 加载中 -->
            <div v-if="matchingLoading" class="matching-loading">
              <div class="spinner"></div>
              <p>正在智能匹配中...</p>
              <p class="matching-subtitle">{{ matchingTitle }}</p>
            </div>

            <!-- 匹配结果 -->
            <div v-else-if="matchingResult && !matchingResult.error" class="modal-content">
              <h2 class="modal-title">
                <i class="fas fa-magic matching-title-icon"></i>
                智能匹配结果
              </h2>
              <p class="matching-source">{{ matchingTitle }}</p>

              <div class="matching-summary">
                <span class="match-summary-item">
                  <i class="fas fa-filter"></i> 候选 {{ matchingResult.filter_info?.candidate_count || 0 }}
                </span>
                <span class="match-summary-item">
                  <i class="fas fa-check-circle"></i> 匹配 {{ matchingResult.total || 0 }}
                </span>
                <span class="match-summary-item" v-if="matchingResult.filter_info?.subject_type">
                  <i class="fas fa-tag"></i> {{ matchingResult.filter_info.subject_type }}
                </span>
                <span class="match-summary-item" v-if="matchingResult.filter_info?.province">
                  <i class="fas fa-map-marker-alt"></i> {{ matchingResult.filter_info.province }}
                </span>
              </div>

              <div v-if="matchingResult.matches && matchingResult.matches.length > 0" class="match-results">
                <div
                  v-for="(m, idx) in matchingResult.matches"
                  :key="idx"
                  class="match-card"
                  :class="matchingType === 'demand' ? 'match-supply-card' : 'match-demand-card'"
                >
                  <div class="match-rank">#{{ idx + 1 }}</div>
                  <div class="match-card-body">
                    <h3 class="match-card-title">
                      {{ matchingType === 'demand' ? m.supply.provider : m.demand.title }}
                    </h3>
                    <div class="match-card-meta">
                      <span v-if="matchingType === 'demand'" class="match-meta-item">
                        <i class="fas fa-map-marker-alt"></i> {{ m.supply.location || '未知' }}
                      </span>
                      <span v-if="matchingType === 'demand'" class="match-meta-item">
                        <i class="fas fa-building"></i> {{ m.supply.subject_type || '未知' }}
                      </span>
                      <span v-if="matchingType === 'demand'" class="match-meta-item">
                        <i class="fas fa-link"></i> {{ truncateText(m.supply.border_fit, 40) }}
                      </span>
                      <span v-if="matchingType === 'supply'" class="match-meta-item">
                        <i class="fas fa-map-marker-alt"></i> {{ m.demand.province || '未知' }}
                      </span>
                      <span v-if="matchingType === 'supply'" class="match-meta-item">
                        <i class="fas fa-flag"></i> {{ m.demand.stage || '待定' }}
                      </span>
                      <span v-if="matchingType === 'supply'" class="match-meta-item">
                        <i class="fas fa-tag"></i> {{ m.demand.supply_tags || '无标签' }}
                      </span>
                    </div>
                    <p v-if="matchingType === 'demand'" class="match-card-desc">
                      {{ truncateText(m.supply.services, 150) }}
                    </p>
                    <p v-else class="match-card-desc">
                      {{ truncateText(m.demand.pain_point || m.demand.description, 150) }}
                    </p>
                    <div class="match-scores">
                      <span class="score-badge total">综合 {{ m.score }}</span>
                      <span class="score-badge">关键词 {{ m.keyword_score }}</span>
                      <span class="score-badge">标签 {{ m.tag_score }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div v-else class="no-match-result">
                <i class="fas fa-search"></i>
                <p>未找到匹配结果</p>
              </div>
            </div>

            <!-- 错误提示 -->
            <div v-else-if="matchingResult && matchingResult.error" class="modal-content">
              <h2 class="modal-title"><i class="fas fa-exclamation-triangle"></i> 匹配失败</h2>
              <p class="error-message">{{ matchingResult.message }}</p>
            </div>
          </div>
        </div>
      </transition>
    </div>

    <AppFooter />
  </div>
</template>

<script setup>
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import { ref, computed, onMounted, watch } from 'vue'
import { matchSuppliesForDemand, matchDemandsForSupply } from '@/api/matching'

/* ---------- Tab 切换 ---------- */
const activeTab = ref('borderDemands')
const itemsPerPage = 5

/* ---------- 边疆需求 & 内地供给状态 ---------- */
const borderDemands = ref([])
const mainlandSupply = ref([])
const selectedBdCategory = ref('全部')
const selectedMsCategory = ref('全部')
const bdPage = ref(1)
const msPage = ref(1)

const selectedItem = ref(null)
const detailType = ref('')

/* ---------- 智能匹配状态 ---------- */
const matchingLoading = ref(false)
const matchingResult = ref(null)
const matchingType = ref('')
const matchingTitle = ref('')

const tabs = computed(() => [
  { key: 'borderDemands', label: '边疆需求侧', icon: 'fas fa-flag', count: borderDemands.value.length },
  { key: 'mainlandSupply', label: '内地供给侧', icon: 'fas fa-hand-holding-heart', count: mainlandSupply.value.length }
])

const borderCategories = computed(() => {
  const ps = new Set(['全部'])
  borderDemands.value.forEach(d => {
    if (d['省/自治区']) ps.add(d['省/自治区'])
  })
  return Array.from(ps)
})

const supplyCategories = computed(() => {
  const ts = new Set(['全部'])
  mainlandSupply.value.forEach(s => {
    if (s['主体类型']) ts.add(s['主体类型'])
  })
  return Array.from(ts)
})

const filteredBorderDemands = computed(() => {
  if (selectedBdCategory.value === '全部') return borderDemands.value
  return borderDemands.value.filter(d => d['省/自治区'] === selectedBdCategory.value)
})

const filteredMainlandSupply = computed(() => {
  if (selectedMsCategory.value === '全部') return mainlandSupply.value
  return mainlandSupply.value.filter(s => s['主体类型'] === selectedMsCategory.value)
})

const bdTotalPages = computed(() => Math.ceil(filteredBorderDemands.value.length / itemsPerPage) || 1)
const msTotalPages = computed(() => Math.ceil(filteredMainlandSupply.value.length / itemsPerPage) || 1)

const bdDisplayRange = computed(() => {
  if (pagedBorderDemands.value.length === 0) return '0-0'
  const start = (bdPage.value - 1) * itemsPerPage + 1
  const end = start + pagedBorderDemands.value.length - 1
  return `${start}-${end}`
})

const msDisplayRange = computed(() => {
  if (pagedMainlandSupply.value.length === 0) return '0-0'
  const start = (msPage.value - 1) * itemsPerPage + 1
  const end = start + pagedMainlandSupply.value.length - 1
  return `${start}-${end}`
})

const pagedBorderDemands = computed(() => {
  const start = (bdPage.value - 1) * itemsPerPage
  return filteredBorderDemands.value.slice(start, start + itemsPerPage)
})

const pagedMainlandSupply = computed(() => {
  const start = (msPage.value - 1) * itemsPerPage
  return filteredMainlandSupply.value.slice(start, start + itemsPerPage)
})

/* ---------- 方法 ---------- */
const switchTab = (key) => {
  activeTab.value = key
  selectedBdCategory.value = '全部'
  selectedMsCategory.value = '全部'
  bdPage.value = 1
  msPage.value = 1
}

const changeBdPage = (delta) => {
  const next = bdPage.value + delta
  if (next >= 1 && next <= bdTotalPages.value) {
    bdPage.value = next
    window.scrollTo({ top: 300, behavior: 'smooth' })
  }
}

const changeMsPage = (delta) => {
  const next = msPage.value + delta
  if (next >= 1 && next <= msTotalPages.value) {
    msPage.value = next
    window.scrollTo({ top: 300, behavior: 'smooth' })
  }
}

const selectBdCategory = (cat) => {
  selectedBdCategory.value = cat
  bdPage.value = 1
}

const selectMsCategory = (cat) => {
  selectedMsCategory.value = cat
  msPage.value = 1
}

const truncateText = (text, max) => {
  if (!text) return ''
  if (text.length <= max) return text
  return text.substring(0, max) + '...'
}

const openDetail = (item, type) => {
  selectedItem.value = item
  detailType.value = type
  document.body.style.overflow = 'hidden'
}

const closeDetail = () => {
  selectedItem.value = null
  document.body.style.overflow = ''
}

/* ---------- 智能匹配 ---------- */
const runMatchSupplies = async (item) => {
  matchingLoading.value = true
  matchingResult.value = null
  matchingType.value = 'demand'
  matchingTitle.value = item['需求标题'] || item['需求ID']
  document.body.style.overflow = 'hidden'
  try {
    const res = await matchSuppliesForDemand(item['需求ID'], { top_k: 5 })
    matchingResult.value = res
  } catch (e) {
    console.error('匹配失败:', e)
    matchingResult.value = { error: true, message: '匹配请求失败，请检查后端服务是否运行' }
  } finally {
    matchingLoading.value = false
  }
}

const runMatchDemands = async (item) => {
  matchingLoading.value = true
  matchingResult.value = null
  matchingType.value = 'supply'
  matchingTitle.value = item['提供方'] || item['供给ID']
  document.body.style.overflow = 'hidden'
  try {
    const res = await matchDemandsForSupply(item['供给ID'], { top_k: 5 })
    matchingResult.value = res
  } catch (e) {
    console.error('匹配失败:', e)
    matchingResult.value = { error: true, message: '匹配请求失败，请检查后端服务是否运行' }
  } finally {
    matchingLoading.value = false
  }
}

const closeMatching = () => {
  matchingResult.value = null
  matchingLoading.value = false
  matchingType.value = ''
  matchingTitle.value = ''
  document.body.style.overflow = ''
}

watch(selectedBdCategory, () => { bdPage.value = 1 })
watch(selectedMsCategory, () => { msPage.value = 1 })

onMounted(async () => {
  try {
    const res = await fetch('/data/achievements.json')
    const data = await res.json()
    borderDemands.value = data.border_demands || []
    mainlandSupply.value = data.mainland_supply || []
  } catch (e) {
    console.error('加载案例数据失败:', e)
  }
})
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #f5f9ff;
}

.page-header {
  background: linear-gradient(135deg, #1a5276 0%, #2980b9 100%);
  color: white;
  padding: 50px 5% 40px;
  text-align: center;
  box-shadow: 0 10px 25px rgba(26, 82, 118, 0.25);
}

.page-header h1 {
  font-size: 2.8rem;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.page-header p {
  font-size: 1.2rem;
  opacity: 0.9;
  max-width: 800px;
  margin: 0 auto;
}

.content-area {
  padding: 30px 5% 60px;
}

.filter-container {
  background: var(--color-bg-card, #fff);
  border-radius: 12px;
  padding: 25px 30px;
  margin-bottom: 30px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
}

.filter-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-title i {
  color: #2980b9;
}

.category-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.category-btn {
  padding: 10px 20px;
  background-color: #f8f9fa;
  border: 2px solid #e0e0e0;
  border-radius: 25px;
  cursor: pointer;
  font-size: 1rem;
  color: #555;
  transition: all 0.3s;
}

.category-btn:hover {
  background-color: #e8e8e8;
  border-color: #bbb;
}

.category-btn.active {
  background-color: #2980b9;
  border-color: #2980b9;
  color: white;
}

.filter-actions {
  display: flex;
  gap: 12px;
  margin-top: 20px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 10px 25px;
  background: linear-gradient(135deg, #1a5276 0%, #2980b9 100%);
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-weight: bold;
  font-size: 0.95rem;
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(41, 128, 185, 0.3);
}

.reset-btn {
  padding: 10px 20px;
  background-color: #f8f9fa;
  border: 2px solid #e0e0e0;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.95rem;
  color: #555;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.2s;
}

.reset-btn:hover {
  background-color: #f0f0f0;
}

.results-info {
  margin-bottom: 25px;
  padding: 15px 20px;
  background-color: #e8f4fd;
  border-radius: 8px;
  color: #1a5276;
  font-weight: 500;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.demands-container {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.demand-card {
  background-color: #fff;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  border-left: 6px solid #2980b9;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.demand-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.12);
}

.demand-title {
  color: #1a5276;
  font-size: 1.8rem;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.demand-info {
  display: flex;
  gap: 30px;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #f0f0f0;
  flex-wrap: wrap;
}

.info-item {
  font-size: 1.05rem;
  color: #555;
  display: flex;
  align-items: center;
  gap: 8px;
}

.info-item i {
  color: #2980b9;
}

.majors-section {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 25px;
}

.majors-title {
  font-size: 1.2rem;
  color: #2c3e50;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.majors-title i {
  color: #2980b9;
}

.majors-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.major-tag {
  background-color: #e3f2fd;
  color: #1565c0;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.9rem;
}

.no-majors {
  color: #999;
  font-style: italic;
  font-size: 0.9rem;
}

.demand-content {
  margin-bottom: 25px;
  color: #444;
  line-height: 1.7;
  padding: 15px 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #2980b9;
}

.content-title {
  font-weight: 600;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #2c3e50;
}

.content-title i {
  color: #2980b9;
}

.contact-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 20px;
  border-top: 1px dashed #e0e0e0;
  flex-wrap: wrap;
  gap: 15px;
}

.contact-details {
  display: flex;
  align-items: center;
  gap: 15px;
  flex-wrap: wrap;
}

.contact-name {
  font-size: 1.3rem;
  font-weight: bold;
  color: #1a5276;
}

.contact-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.contact-tag {
  background-color: #e8f4fd;
  color: #1a5276;
  padding: 5px 14px;
  border-radius: 20px;
  font-size: 0.9rem;
}

.contact-btn {
  background: linear-gradient(135deg, #1a5276 0%, #2980b9 100%);
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 5px 15px rgba(41, 128, 185, 0.3);
  transition: background 0.2s, transform 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.contact-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(41, 128, 185, 0.4);
}

.divider {
  height: 2px;
  background: linear-gradient(to right, transparent, #2980b9, transparent);
  margin: 30px 0;
  border: none;
}

.status-tag {
  display: inline-block;
  padding: 4px 14px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: bold;
}

.status-open {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.status-closed {
  background-color: #ffebee;
  color: #c62828;
}

.loading {
  text-align: center;
  padding: 60px;
  color: #777;
}

.spinner {
  border: 4px solid #e0e0e0;
  border-top: 4px solid #2980b9;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-box {
  text-align: center;
  padding: 50px;
  color: #c0392b;
  background-color: #ffebee;
  border-radius: 12px;
  margin: 20px 0;
}

.error-box i {
  font-size: 2.5rem;
  margin-bottom: 15px;
  color: #c0392b;
}

.error-box p {
  font-size: 1.1rem;
  margin-bottom: 20px;
}

.reload-btn {
  padding: 10px 24px;
  background: #2980b9;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: background 0.2s;
}

.reload-btn:hover {
  background: #1a5276;
}

.no-data {
  text-align: center;
  padding: 60px;
  color: #777;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  margin: 20px 0;
}

.no-data i {
  font-size: 4rem;
  margin-bottom: 20px;
  color: #ddd;
}

.no-data h3 {
  font-size: 1.5rem;
  margin-bottom: 10px;
  color: #2c3e50;
}

.no-data p {
  color: #999;
  margin-bottom: 20px;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 40px;
}

.pagination {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
  justify-content: center;
}

.page-btn {
  padding: 8px 16px;
  background-color: #fff;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.95rem;
  min-width: 40px;
  text-align: center;
  color: #555;
}

.page-btn:hover:not(.disabled) {
  background-color: #f0f0f0;
  border-color: #2980b9;
  color: #2980b9;
}

.page-btn.active {
  background-color: #2980b9;
  color: white;
  border-color: #2980b9;
}

.page-btn.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background-color: #f8f9fa;
}

.page-info {
  color: #999;
  font-size: 0.9rem;
  margin: 0 12px;
}

@media (max-width: 768px) {
  .page-header h1 {
    font-size: 2.2rem;
    flex-direction: column;
    gap: 10px;
  }

  .page-header p {
    font-size: 1rem;
  }

  .category-filter {
    justify-content: center;
  }

  .category-btn {
    padding: 8px 16px;
    font-size: 0.9rem;
  }

  .filter-actions {
    justify-content: center;
  }

  .demand-info {
    flex-direction: column;
    gap: 10px;
  }

  .contact-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }

  .contact-btn {
    align-self: stretch;
    text-align: center;
    justify-content: center;
  }

  .pagination {
    flex-wrap: wrap;
    justify-content: center;
  }

  .page-info {
    order: -1;
    width: 100%;
    text-align: center;
    margin-bottom: 10px;
  }

  .demand-card {
    padding: 20px;
  }

  .demand-title {
    font-size: 1.4rem;
  }
}

/* ---------- Tab 栏 ---------- */
.tab-bar {
  display: flex;
  gap: 5px;
  margin-bottom: 25px;
  background: #eef5fc;
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
  color: #2980b9;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

.tab-count {
  background: #2980b922;
  color: #2980b9;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.8rem;
}

.tab-btn.active .tab-count {
  background: #2980b9;
  color: white;
}

/* ---------- 搜索与筛选工具栏 ---------- */
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
  border-color: #2980b9;
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
  border-color: #2980b9;
  outline: none;
}

/* ---------- 边疆需求 & 内地供给卡片 ---------- */
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
  transform: translateY(-4px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
}

.demand-side-card {
  border-left: 6px solid #2980b9;
}

.supply-side-card {
  border-left: 6px solid #27ae60;
}

.card-body {
  padding: 18px 22px;
}

.card-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.card-tag {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 0.78rem;
  font-weight: 600;
}

.tag-demand {
  background: #2980b922;
  color: #2980b9;
}

.tag-supply {
  background: #27ae6022;
  color: #27ae60;
}

.card-id {
  font-size: 0.8rem;
  color: #aaa;
  font-weight: 500;
}

.card-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 10px;
  line-height: 1.4;
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
}

.card-sub {
  font-size: 0.85rem;
  color: #888;
  line-height: 1.5;
  margin-bottom: 10px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
  border-top: 1px solid #f0f0f0;
}

.view-detail {
  font-size: 0.85rem;
  color: #2980b9;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: gap 0.3s;
}

.case-card:hover .view-detail {
  gap: 8px;
}

.no-data-icon {
  font-size: 3rem;
  margin-bottom: 15px;
  color: #ddd;
}

/* ---------- 详情弹窗 ---------- */
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
  background: #2980b9;
  color: white;
}

.modal-content {
  width: 100%;
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
  background: #2980b922;
  color: #2980b9;
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
  color: #2980b9;
  margin-bottom: 6px;
  padding-bottom: 4px;
  border-bottom: 2px solid #2980b933;
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

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

/* ---------- 边疆需求/内地供给 卡片样式 ---------- */
.border-demand-card {
  border-left: 6px solid #2980b9;
}

.supply-demand-card {
  border-left: 6px solid #27ae60;
}

.card-id {
  font-size: 0.8rem;
  color: #aaa;
  font-weight: 500;
  margin-left: auto;
}

.bd-stage-tag {
  background-color: #e8f4fd;
  color: #1a5276;
}

.ms-type-tag {
  background-color: #e8f8e8;
  color: #1b7d1b;
}

.detail-block {
  margin-bottom: 14px;
  padding: 12px 16px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #2980b9;
}

.supply-demand-card .detail-block {
  border-left-color: #27ae60;
}

.detail-block-label {
  font-size: 0.88rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.detail-block-label i {
  color: #2980b9;
}

.supply-demand-card .detail-block-label i {
  color: #27ae60;
}

.detail-block-content {
  font-size: 0.9rem;
  color: #555;
  line-height: 1.6;
}

.supply-cat-btn.active {
  background-color: #27ae60;
  border-color: #27ae60;
  color: white;
}

.supply-contact-btn {
  background: linear-gradient(135deg, #1b7d1b 0%, #27ae60 100%) !important;
  box-shadow: 0 5px 15px rgba(39, 174, 96, 0.3) !important;
}

.supply-contact-btn:hover {
  box-shadow: 0 8px 20px rgba(39, 174, 96, 0.4) !important;
}

@media (max-width: 768px) {
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

/* ---------- 智能匹配按钮 ---------- */
.contact-btns {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.match-btn {
  background: linear-gradient(135deg, #6a1b9a 0%, #8e24aa 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 25px;
  font-size: 0.95rem;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 5px 15px rgba(142, 36, 170, 0.3);
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
}

.match-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(142, 36, 170, 0.4);
}

.match-demand-btn {
  background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%);
  box-shadow: 0 5px 15px rgba(46, 125, 50, 0.3);
}

.match-demand-btn:hover {
  box-shadow: 0 8px 20px rgba(46, 125, 50, 0.4);
}

/* ---------- 智能匹配弹窗 ---------- */
.matching-modal {
  max-width: 720px;
}

.matching-loading {
  text-align: center;
  padding: 60px 20px;
}

.matching-loading p {
  color: #555;
  font-size: 1.1rem;
  margin-top: 15px;
}

.matching-loading .matching-subtitle {
  color: #999;
  font-size: 0.95rem;
  margin-top: 8px;
}

.matching-title-icon {
  color: #8e24aa;
  margin-right: 8px;
}

.matching-source {
  color: #666;
  font-size: 0.95rem;
  margin-bottom: 20px;
  padding: 10px 16px;
  background: #f5f0fa;
  border-radius: 8px;
  border-left: 4px solid #8e24aa;
}

.matching-summary {
  display: flex;
  gap: 16px;
  margin-bottom: 25px;
  flex-wrap: wrap;
  padding: 12px 16px;
  background: #f0f4f8;
  border-radius: 10px;
}

.match-summary-item {
  font-size: 0.9rem;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 500;
}

.match-summary-item i {
  color: #2980b9;
}

.match-results {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.match-card {
  display: flex;
  gap: 16px;
  padding: 18px;
  background: #f8f9fa;
  border-radius: 12px;
  border-left: 5px solid #8e24aa;
  transition: box-shadow 0.3s, transform 0.3s;
}

.match-card:hover {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  transform: translateX(4px);
}

.match-supply-card {
  border-left-color: #8e24aa;
}

.match-demand-card {
  border-left-color: #27ae60;
}

.match-rank {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #8e24aa, #ba2cd0);
  color: white;
  font-weight: 700;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.match-demand-card .match-rank {
  background: linear-gradient(135deg, #1b5e20, #2e7d32);
}

.match-card-body {
  flex: 1;
  min-width: 0;
}

.match-card-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: #1a5276;
  margin-bottom: 8px;
  line-height: 1.4;
}

.match-card-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.match-meta-item {
  font-size: 0.82rem;
  color: #777;
  display: flex;
  align-items: center;
  gap: 5px;
}

.match-meta-item i {
  color: #aaa;
}

.match-card-desc {
  font-size: 0.88rem;
  color: #555;
  line-height: 1.6;
  margin-bottom: 10px;
}

.match-scores {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.score-badge {
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 0.78rem;
  font-weight: 600;
  background: #f0f0f0;
  color: #666;
}

.score-badge.total {
  background: #8e24aa22;
  color: #8e24aa;
  font-weight: 700;
}

.match-demand-card .score-badge.total {
  background: #27ae6022;
  color: #27ae60;
}

.no-match-result {
  text-align: center;
  padding: 50px 20px;
  color: #999;
}

.no-match-result i {
  font-size: 2.5rem;
  margin-bottom: 15px;
  color: #ddd;
}

.error-message {
  color: #c0392b;
  font-size: 1rem;
  padding: 20px;
  background: #ffebee;
  border-radius: 8px;
  text-align: center;
}

@media (max-width: 768px) {
  .contact-btns {
    flex-direction: column;
    width: 100%;
  }

  .match-btn,
  .contact-btn {
    text-align: center;
    justify-content: center;
  }

  .match-card {
    flex-direction: column;
    gap: 10px;
  }

  .match-rank {
    align-self: flex-start;
  }
}
</style>
