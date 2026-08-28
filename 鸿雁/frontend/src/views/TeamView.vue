<template>
  <div class="page">
    <AppHeader />

    <!-- 页面头部 -->
    <section class="page-header">
      <div class="container">
        <h1>
          <i class="fas fa-users"></i> 团队信息
          <i class="fas fa-handshake"></i>
        </h1>
        <p>浏览平台团队与高校科研团队信息，了解各团队的专业领域和技术成果</p>
      </div>
    </section>

    <div class="container content-area">
      <!-- 分类筛选区域 -->
      <div class="filter-container">
        <div class="filter-title">
          <i class="fas fa-filter"></i> 按专业领域筛选
        </div>
        <div class="category-filter">
          <button
            v-for="cat in categories"
            :key="cat"
            class="category-btn"
            :class="{ active: selectedCategory === cat }"
            @click="selectCategory(cat)"
          >
            {{ cat }}
          </button>
        </div>
        <div class="filter-actions">
          <button class="filter-btn" @click="applyFilter">
            <i class="fas fa-check"></i> 应用筛选
          </button>
          <button class="reset-btn" @click="resetFilter">
            <i class="fas fa-redo"></i> 重置筛选
          </button>
        </div>
      </div>

      <!-- 结果信息 -->
      <div v-if="teams.length > 0" class="results-info">
        <span>找到 <strong>{{ total }}</strong> 个相关团队</span>
        <span>显示第 {{ displayRange }}</span>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>正在加载团队数据...</p>
      </div>

      <!-- 错误显示 -->
      <div v-if="error" class="error-box">
        <i class="fas fa-exclamation-triangle"></i>
        <p>{{ errorMessage }}</p>
        <button class="reload-btn" @click="loadData">
          <i class="fas fa-sync-alt"></i> 重新加载
        </button>
      </div>

      <!-- 团队列表 -->
      <main v-if="!loading && !error" class="teams-container">
        <!-- 无数据 -->
        <div v-if="teams.length === 0" class="no-data">
          <i class="fas fa-users"></i>
          <h3>暂无团队信息</h3>
          <p v-if="selectedCategory !== '全部'">在"{{ selectedCategory }}"分类下没有找到团队信息</p>
          <p v-else>当前没有团队提交信息</p>
          <button v-if="selectedCategory !== '全部'" class="reset-btn" @click="resetFilter">
            <i class="fas fa-redo"></i> 返回全部团队
          </button>
        </div>

        <!-- 团队卡片 -->
        <template v-else>
          <article
            v-for="(team, index) in teams"
            :key="team.id || index"
            class="team-card"
            :class="{ 'sdu-card': team.source === 'sdu' }"
          >
            <h2 class="team-title">
              {{ team.team_name || '未命名团队' }}
              <span class="status-tag" :class="{ 'sdu-cat-tag': team.source === 'sdu' }">
                {{ team.source === 'sdu' ? (team.category || team.team_specialty || '未指定') : (team.team_specialty || '未指定') }}
              </span>
              <span v-if="team.source === 'sdu'" class="source-badge sdu-badge">山大科研</span>
              <span v-else class="source-badge platform-badge">平台团队</span>
            </h2>

            <div class="team-info">
              <div class="team-leader">
                <i class="fas fa-user-graduate"></i>
                负责人: {{ team.source === 'sdu' ? (team.leader || '未知') : (team.leader_name || '未知') }}
                <span v-if="team.source !== 'sdu' && team.student_id">({{ team.student_id }})</span>
              </div>
              <div class="team-university">
                <i class="fas fa-school"></i>
                {{ team.source === 'sdu' ? (team.department || '未知学院') : (team.university || '未知高校') }}
              </div>
              <div class="team-specialty">
                {{ team.source === 'sdu' ? (team.research_field || '未指定') : (team.team_specialty || '未指定') }}
              </div>
            </div>

            <!-- SDU 团队：富信息区块 -->
            <template v-if="team.source === 'sdu'">
              <div v-if="team.title" class="sdu-detail-block">
                <div class="sdu-detail-label"><i class="fas fa-award"></i> 人才头衔</div>
                <div class="sdu-detail-content">{{ team.title }}</div>
              </div>

              <div class="sdu-grid">
                <div v-if="team.patents" class="sdu-detail-block">
                  <div class="sdu-detail-label"><i class="fas fa-file-alt"></i> 代表性专利</div>
                  <div class="sdu-detail-content">{{ team.patents }}</div>
                </div>
                <div v-if="team.achievements" class="sdu-detail-block">
                  <div class="sdu-detail-label"><i class="fas fa-cogs"></i> 核心技术成果</div>
                  <div class="sdu-detail-content">{{ team.achievements }}</div>
                </div>
                <div v-if="team.awards" class="sdu-detail-block">
                  <div class="sdu-detail-label"><i class="fas fa-trophy"></i> 获奖/项目级别</div>
                  <div class="sdu-detail-content">{{ team.awards }}</div>
                </div>
                <div v-if="team.western_scenario" class="sdu-detail-block">
                  <div class="sdu-detail-label"><i class="fas fa-map-marked-alt"></i> 可服务西部场景</div>
                  <div class="sdu-detail-content">{{ team.western_scenario }}</div>
                </div>
                <div v-if="team.application" class="sdu-detail-block">
                  <div class="sdu-detail-label"><i class="fas fa-bullseye"></i> 具体应用方向</div>
                  <div class="sdu-detail-content">{{ team.application }}</div>
                </div>
                <div v-if="team.maturity" class="sdu-detail-block">
                  <div class="sdu-detail-label"><i class="fas fa-chart-line"></i> 技术成熟度</div>
                  <div class="sdu-detail-content">{{ team.maturity }}</div>
                </div>
              </div>

              <div v-if="team.cases" class="sdu-detail-block">
                <div class="sdu-detail-label"><i class="fas fa-handshake"></i> 已转化/合作案例</div>
                <div class="sdu-detail-content">{{ team.cases }}</div>
              </div>

              <div v-if="team.remark" class="team-description">
                <p>{{ team.remark }}</p>
              </div>
            </template>

            <!-- 平台团队：成员与详情 -->
            <template v-else>
              <div class="team-details">
                <div class="detail-item">负责人电话: {{ team.leader_contact || '未提供' }}</div>
                <div class="detail-item">负责人邮箱: {{ team.leader_email || '未提供' }}</div>
                <div v-if="team.teacher_name" class="detail-item">
                  指导老师: {{ team.teacher_name }}
                </div>
              </div>

              <div class="members-section">
                <div class="members-title">
                  <i class="fas fa-user"></i>
                  团队成员 ({{ memberNames(team).length }}人)
                </div>
                <div class="members-list" v-if="memberNames(team).length > 0">
                  <span
                    v-for="(member, mi) in memberNames(team)"
                    :key="mi"
                    class="member-tag"
                  >{{ member }}</span>
                </div>
                <p v-else class="no-members">暂无成员信息</p>
              </div>

              <div v-if="getTeacherInfo(team).length > 0" class="teacher-section">
                <div class="teacher-title">
                  <i class="fas fa-chalkboard-teacher"></i>
                  指导老师信息
                </div>
                <div class="teacher-info">
                  <div
                    v-for="(teacher, ti) in getTeacherInfo(team)"
                    :key="ti"
                    class="teacher-item"
                  >
                    <strong>{{ teacher['Teacher Name'] || '未命名' }}</strong><br />
                    联系方式: {{ teacher['Teacher Contact Information'] || '未提供' }}
                  </div>
                </div>
              </div>

              <div class="team-description" v-if="team.team_description">
                <p>{{ team.team_description }}</p>
              </div>
            </template>

            <!-- 底部联系区域（两种团队共用） -->
            <div class="contact-info">
              <div class="contact-details">
                <span class="contact-name">
                  {{ team.source === 'sdu' ? (team.leader || '未知') : (team.leader_name || '未知') }}
                </span>
                <div class="contact-tags">
                  <span v-if="team.source === 'sdu'" class="contact-tag">{{ team.department || '山东大学' }}</span>
                  <span v-else class="contact-tag">负责人</span>
                  <span class="contact-tag">{{ team.source === 'sdu' ? (team.category || '科研团队') : (team.university || '未知高校') }}</span>
                  <span class="contact-tag">{{ team.source === 'sdu' ? (team.maturity || '未标注') : (team.team_specialty || '未指定') }}</span>
                </div>
              </div>
              <a
                v-if="team.source === 'sdu' && team.link"
                :href="team.link"
                target="_blank"
                class="contact-btn sdu-link-btn"
              >
                <i class="fas fa-external-link-alt"></i> 查看详情
              </a>
              <button
                v-else
                class="contact-btn"
                @click="contactTeam(team)"
              >
                <i class="fas fa-envelope"></i> 联系团队
              </button>
            </div>

            <hr
              v-if="index < teams.length - 1"
              class="divider"
            />
          </article>
        </template>
      </main>

      <!-- 分页 -->
      <div v-if="totalPages > 1" class="pagination-container">
        <div class="pagination">
          <button
            class="page-btn"
            :class="{ disabled: currentPage === 1 }"
            @click="changePage(currentPage - 1)"
          >
            <i class="fas fa-chevron-left"></i>
          </button>
          <button
            v-for="p in totalPages"
            :key="p"
            class="page-btn"
            :class="{ active: p === currentPage }"
            @click="changePage(p)"
          >{{ p }}</button>
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
    </div>

    <AppFooter />
  </div>
</template>

<script setup>
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import { ref, computed, onMounted } from 'vue'
import { listTeams } from '@/api/teams'
import { ElMessage } from 'element-plus'
import sduTeamsData from '@/data/sdu_teams.json'

const SDU_CATEGORIES = ['农业种植与加工', '能源与光伏', '产业升级与智能制造', 'AI训练与创新成果']

const teams = ref([])
const total = ref(0)
const totalPages = ref(1)
const loading = ref(false)
const error = ref(false)
const errorMessage = ref('')
const selectedCategory = ref('全部')
const currentPage = ref(1)
const itemsPerPage = 4
let mergedCache = null

const categories = [
  '全部',
  '医疗健康',
  '基础建设',
  '教育民生',
  '基层治理',
  '文旅',
  '环境',
  '农业种植与加工',
  '能源与光伏',
  '产业升级与智能制造',
  'AI训练与创新成果'
]

const memberNames = (team) => (team.members || []).map(m => m.member_name)

const displayRange = computed(() => {
  if (teams.value.length === 0) return '0-0'
  const start = (currentPage.value - 1) * itemsPerPage + 1
  const end = start + teams.value.length - 1
  return `${start}-${end}`
})

const selectCategory = (cat) => {
  selectedCategory.value = cat
  currentPage.value = 1
  if (cat !== '全部') mergedCache = null
  loadData()
}

const applyFilter = () => {
  currentPage.value = 1
  mergedCache = null
  loadData()
  ElMessage.success('筛选已应用')
}

const resetFilter = () => {
  selectedCategory.value = '全部'
  currentPage.value = 1
  mergedCache = null
  loadData()
}

const changePage = (page) => {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
  const cat = selectedCategory.value
  if (cat === '全部' && mergedCache) {
    const start = (currentPage.value - 1) * itemsPerPage
    teams.value = mergedCache.slice(start, start + itemsPerPage)
  } else if (SDU_CATEGORIES.includes(cat)) {
    const filtered = sduTeamsData.filter(t => t.category === cat).map(t => ({ ...t, source: 'sdu' }))
    const start = (currentPage.value - 1) * itemsPerPage
    teams.value = filtered.slice(start, start + itemsPerPage)
  } else {
    loadData()
  }
  const filterEl = document.querySelector('.filter-container')
  if (filterEl) {
    window.scrollTo({ top: filterEl.offsetTop - 20, behavior: 'smooth' })
  }
}

const getTeacherInfo = (team) => {
  if (team.teacher_name) {
    return [{ 'Teacher Name': team.teacher_name, 'Teacher Contact Information': team.teacher_contact || '未提供' }]
  }
  return []
}

const contactTeam = (team) => {
  const teamName = team.team_name || '未命名团队'
  const contact = team.leader_contact || '未提供'
  const email = team.leader_email || ''
  ElMessage({
    message: `联系团队: ${teamName} | 电话: ${contact}${email ? ' | 邮箱: ' + email : ''}`,
    type: 'info',
    duration: 5000
  })
}

const loadData = async () => {
  loading.value = true
  error.value = false

  try {
    const cat = selectedCategory.value

    if (SDU_CATEGORIES.includes(cat)) {
      const filtered = sduTeamsData
        .filter(t => t.category === cat)
        .map(t => ({ ...t, source: 'sdu' }))
      total.value = filtered.length
      totalPages.value = Math.ceil(filtered.length / itemsPerPage) || 1
      const start = (currentPage.value - 1) * itemsPerPage
      teams.value = filtered.slice(start, start + itemsPerPage)
    } else if (cat === '全部') {
      if (!mergedCache) {
        const apiResult = await listTeams({ page: 1, page_size: 100 })
        const apiTeams = (apiResult.items || []).map(t => ({ ...t, source: 'platform' }))
        const sduTeams = sduTeamsData.map(t => ({ ...t, source: 'sdu' }))
        mergedCache = [...sduTeams, ...apiTeams]
      }
      total.value = mergedCache.length
      totalPages.value = Math.ceil(mergedCache.length / itemsPerPage) || 1
      const start = (currentPage.value - 1) * itemsPerPage
      teams.value = mergedCache.slice(start, start + itemsPerPage)
    } else {
      const params = { page: currentPage.value, page_size: itemsPerPage, category: cat }
      const result = await listTeams(params)
      teams.value = (result.items || []).map(t => ({ ...t, source: 'platform' }))
      total.value = result.total || 0
      totalPages.value = result.total_pages || 1
    }
  } catch (err) {
    console.error('加载数据失败:', err)
    error.value = true
    errorMessage.value = `数据加载失败: ${err.message || '请稍后重试'}`
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: var(--paper);
}

/* ---------- 页面头部 ---------- */
.page-header {
  background: linear-gradient(135deg, var(--color-primary-darker) 0%, var(--color-primary-dark) 100%);
  color: white;
  padding: 50px 5% 40px;
  text-align: center;
  box-shadow: 0 10px 25px rgba(156, 12, 19, 0.25);
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

/* ---------- 筛选区域 ---------- */
.filter-container {
  background: var(--color-bg-card);
  border-radius: var(--radius-md);
  padding: 25px 30px;
  margin-bottom: 30px;
  box-shadow: var(--shadow-md);
}

.filter-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-title i {
  color: var(--color-primary-darker);
}

.category-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.category-btn {
  padding: 10px 20px;
  background-color: var(--color-bg-alt);
  border: 2px solid var(--color-border);
  border-radius: var(--radius-pill);
  cursor: pointer;
  font-size: 1rem;
  font-family: var(--font-family);
  color: var(--color-text-light);
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 6px;
}

.category-btn:hover {
  background-color: #e8e8e8;
  border-color: #ccc;
}

.category-btn.active {
  background-color: var(--color-primary-darker);
  border-color: var(--color-primary-darker);
  color: white;
}

.category-count {
  font-size: 0.85em;
  background: rgba(255, 255, 255, 0.2);
  padding: 2px 8px;
  border-radius: 12px;
  margin-left: 4px;
}

.category-btn.active .category-count {
  background: rgba(255, 255, 255, 0.3);
}

.filter-actions {
  display: flex;
  gap: 12px;
  margin-top: 20px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 10px 25px;
  background: linear-gradient(135deg, var(--color-primary-darker) 0%, var(--color-primary-dark) 100%);
  color: white;
  border: none;
  border-radius: var(--radius-pill);
  cursor: pointer;
  font-weight: bold;
  font-family: var(--font-family);
  font-size: 0.95rem;
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(156, 12, 19, 0.3);
}

.reset-btn {
  padding: 10px 20px;
  background-color: var(--paper-2);
  border: 2px solid var(--color-border);
  border-radius: var(--radius-pill);
  cursor: pointer;
  font-weight: 500;
  font-family: var(--font-family);
  font-size: 0.95rem;
  color: var(--color-text-light);
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.2s;
}

.reset-btn:hover {
  background-color: var(--color-bg-alt);
}

/* ---------- 结果信息 ---------- */
.results-info {
  margin-bottom: 25px;
  padding: 15px 20px;
  background-color: var(--color-primary-light);
  border-radius: var(--radius-sm);
  color: var(--color-primary-darker);
  font-weight: 500;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* ---------- 团队列表 ---------- */
.teams-container {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.team-card {
  background-color: var(--color-bg-card);
  border-radius: var(--radius-md);
  padding: 30px;
  box-shadow: var(--shadow-lg);
  border-left: 6px solid var(--color-primary-darker);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.team-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.12);
}

.team-title {
  color: var(--color-primary-darker);
  font-size: 1.8rem;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.team-title::before {
  content: "\f0c0";
  font-family: "Font Awesome 6 Free";
  font-weight: 900;
  font-size: 1.5rem;
}

.team-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--color-border);
  flex-wrap: wrap;
  gap: 10px;
}

.team-leader {
  font-size: 1.1rem;
  color: var(--color-text-light);
  display: flex;
  align-items: center;
  gap: 8px;
}

.team-leader i {
  color: var(--color-accent);
}

.team-university {
  font-size: 1.1rem;
  color: var(--color-text-light);
  display: flex;
  align-items: center;
  gap: 8px;
}

.team-university i {
  color: var(--color-accent);
}

.team-specialty {
  font-size: 1.4rem;
  color: var(--color-primary);
  font-weight: bold;
}

.team-details {
  display: flex;
  gap: 30px;
  margin-bottom: 25px;
  flex-wrap: wrap;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1rem;
  color: var(--color-text-light);
}

.detail-item::before {
  content: "\2022";
  color: var(--color-primary-darker);
  font-weight: bold;
  font-size: 1.2rem;
}

.members-section {
  background-color: var(--color-bg-alt);
  border-radius: var(--radius-sm);
  padding: 20px;
  margin-bottom: 25px;
}

.members-title {
  font-size: 1.2rem;
  color: var(--color-text);
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.members-title i {
  color: var(--color-accent);
}

.members-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.member-tag {
  background-color: var(--color-accent-light);
  color: var(--color-accent-dark);
  padding: 6px 14px;
  border-radius: var(--radius-pill);
  font-size: 0.9rem;
}

.no-members {
  color: var(--color-text-muted);
  font-style: italic;
  font-size: 0.9rem;
}

.teacher-section {
  background-color: var(--color-primary-light);
  border-radius: var(--radius-sm);
  padding: 20px;
  margin-bottom: 25px;
}

.teacher-title {
  font-size: 1.2rem;
  color: var(--color-text);
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.teacher-title i {
  color: var(--color-accent);
}

.teacher-info {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.teacher-item {
  background-color: var(--color-bg-card);
  padding: 12px 18px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border);
  font-size: 0.95rem;
  color: var(--color-text-light);
}

.team-description {
  margin-bottom: 25px;
  color: var(--color-text-light);
  line-height: 1.7;
  padding: 15px 20px;
  background-color: var(--color-bg-alt);
  border-radius: var(--radius-sm);
  border-left: 4px solid var(--color-primary-darker);
}

.contact-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 20px;
  border-top: 1px dashed var(--color-border);
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
  color: var(--color-primary-darker);
}

.contact-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.contact-tag {
  background-color: var(--color-primary-light);
  color: var(--color-primary-darker);
  padding: 5px 14px;
  border-radius: var(--radius-pill);
  font-size: 0.9rem;
}

.contact-btn {
  background: linear-gradient(135deg, var(--color-primary-darker) 0%, var(--color-primary-dark) 100%);
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: var(--radius-pill);
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  font-family: var(--font-family);
  box-shadow: 0 5px 15px rgba(156, 12, 19, 0.3);
  transition: background 0.2s, transform 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.contact-btn:hover {
  background: linear-gradient(135deg, var(--color-primary-dark) 0%, #4d0609 100%);
  transform: translateY(-2px);
}

.divider {
  height: 2px;
  background: linear-gradient(to right, transparent, var(--color-primary-darker), transparent);
  margin: 30px 0;
  border: none;
}

/* ---------- 状态标签 ---------- */
.status-tag {
  display: inline-block;
  padding: 4px 14px;
  border-radius: var(--radius-pill);
  font-size: 0.85rem;
  font-weight: bold;
  background-color: var(--color-primary-light);
  color: var(--color-primary-darker);
}

/* ---------- 加载状态 ---------- */
.loading {
  text-align: center;
  padding: 60px;
  color: var(--color-text-light);
}

.spinner {
  border: 4px solid var(--color-border);
  border-top: 4px solid var(--color-primary-darker);
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

/* ---------- 错误 ---------- */
.error-box {
  text-align: center;
  padding: 50px;
  color: var(--color-primary);
  background-color: var(--color-primary-light);
  border-radius: var(--radius-md);
  margin: 20px 0;
}

.error-box i {
  font-size: 2.5rem;
  margin-bottom: 15px;
  color: var(--color-primary);
}

.error-box p {
  font-size: 1.1rem;
  margin-bottom: 20px;
}

.reload-btn {
  padding: 10px 24px;
  background: var(--color-primary-darker);
  color: white;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-family: var(--font-family);
  font-size: 0.95rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: background 0.2s;
}

.reload-btn:hover {
  background: var(--color-primary-dark);
}

/* ---------- 无数据 ---------- */
.no-data {
  text-align: center;
  padding: 60px;
  color: var(--color-text-light);
  background-color: var(--color-bg-card);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  margin: 20px 0;
}

.no-data i {
  font-size: 4rem;
  margin-bottom: 20px;
  color: var(--color-border);
}

.no-data h3 {
  font-size: 1.5rem;
  margin-bottom: 10px;
  color: var(--color-text);
}

.no-data p {
  color: var(--color-text-muted);
  margin-bottom: 20px;
}

/* ---------- 分页 ---------- */
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
  background-color: var(--color-bg-card);
  border: 1px solid #d1d5db;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.95rem;
  font-family: var(--font-family);
  min-width: 40px;
  text-align: center;
  color: var(--color-text-light);
}

.page-btn:hover:not(.disabled) {
  background-color: var(--color-bg-alt);
  border-color: var(--color-primary-darker);
  color: var(--color-primary-darker);
}

.page-btn.active {
  background-color: var(--color-primary-darker);
  color: white;
  border-color: var(--color-primary-darker);
}

.page-btn.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background-color: var(--color-bg-alt);
}

.page-info {
  color: var(--color-text-muted);
  font-size: 0.9rem;
  margin: 0 12px;
}

/* ---------- 响应式 ---------- */
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

  .team-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .team-details {
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

  .team-card {
    padding: 20px;
  }

  .team-title {
    font-size: 1.4rem;
  }

  .sdu-grid {
    grid-template-columns: 1fr !important;
  }
}

/* ---------- 来源徽章 ---------- */
.source-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

.sdu-badge {
  background: linear-gradient(135deg, var(--color-primary-dark), var(--color-primary));
  color: white;
}

.platform-badge {
  background: linear-gradient(135deg, var(--color-primary-darker), var(--color-primary-dark));
  color: white;
}

/* ---------- 山大科研团队卡片 ---------- */
.sdu-card {
  border-left: 6px solid var(--color-primary);
}

.sdu-cat-tag {
  background: var(--color-primary-light) !important;
  color: var(--color-primary-dark) !important;
}

.sdu-detail-block {
  margin-bottom: 16px;
  padding: 14px 18px;
  background-color: var(--color-bg-alt);
  border-radius: var(--radius-sm);
  border-left: 4px solid var(--color-primary);
}

.sdu-detail-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-primary-dark);
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.sdu-detail-label i {
  color: var(--color-primary);
}

.sdu-detail-content {
  font-size: 0.92rem;
  color: var(--color-text-light);
  line-height: 1.6;
}

.sdu-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.sdu-grid .sdu-detail-block {
  margin-bottom: 0;
}

.sdu-link-btn {
  background: linear-gradient(135deg, var(--color-primary-dark) 0%, var(--color-primary) 100%) !important;
  box-shadow: 0 5px 15px rgba(41, 128, 185, 0.3) !important;
  text-decoration: none;
  display: inline-flex;
}

.sdu-link-btn:hover {
  background: linear-gradient(135deg, #154360 0%, #1f6b8a 100%) !important;
  transform: translateY(-2px);
}
</style>
