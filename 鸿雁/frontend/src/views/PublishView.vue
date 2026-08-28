<template>
  <div class="page">
    <AppHeader />

    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container hero-grid">
        <div class="hero-card">
          <h1>连接地方需求，赋能边疆发展——山大一体化平台</h1>
          <p class="hero-desc">需求 · 匹配 · 转型 · 升级</p>
          <div class="cta-row">
            <router-link to="/register/enterprise" class="btn primary">
              <i class="fas fa-paper-plane"></i> 发布需求（地方/企业）
            </router-link>
            <router-link to="/register/personal" class="btn primary">
              <i class="fas fa-user-plus"></i> 发布招募（队长）
            </router-link>
            <router-link to="/team" class="btn primary">
              <i class="fas fa-users"></i> 加入队伍
            </router-link>
          </div>

          <div class="board">
            <div class="stat" v-for="stat in stats" :key="stat.label">
              <div class="num">{{ stat.value }}</div>
              <div class="label">{{ stat.label }}</div>
            </div>
          </div>
        </div>

        <div class="hero-right">
          <div class="carousel">
            <div
              v-for="(slide, i) in slides"
              :key="i"
              class="slide"
              :class="slide.cls"
              :style="{ transform: `translateX(${(i - currentSlide) * 100}%)` }"
            >
              {{ slide.text }}
            </div>
            <div class="dots">
              <span
                v-for="(slide, i) in slides"
                :key="i"
                class="dot"
                :class="{ active: i === currentSlide }"
                @click="goToSlide(i)"
              ></span>
            </div>
          </div>

          <div class="search-row">
            <button class="btn icon-btn" @click="prevSlide">
              <i class="fas fa-chevron-left"></i>
            </button>
            <button class="btn icon-btn" @click="nextSlide">
              <i class="fas fa-chevron-right"></i>
            </button>
            <input
              v-model="searchQuery"
              placeholder="按项目/地区/类型搜索需求"
              class="search-input"
              @keyup.enter="handleSearch"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- 需求发布表单 -->
    <section class="section section-alt">
      <div class="container">
        <h2 class="section-title">
          <i class="fas fa-paper-plane"></i> 发布实践需求
        </h2>
        <div class="demand-form-card">
          <div class="form-row">
            <div class="form-group">
              <label>机构名称 <span class="required">*</span></label>
              <input v-model="demandForm.org_name" class="form-input" placeholder="请输入机构名称" />
            </div>
            <div class="form-group">
              <label>机构类型 <span class="required">*</span></label>
              <select v-model="demandForm.org_type" class="form-input">
                <option>政府机构</option>
                <option>企业单位</option>
                <option>事业单位</option>
                <option>社会组织</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>实践地点 <span class="required">*</span></label>
              <input v-model="demandForm.internship_location" class="form-input" placeholder="省/市/区" />
            </div>
            <div class="form-group">
              <label>预计时间</label>
              <input v-model="demandForm.estimated_time" class="form-input" placeholder="如：3个月" />
            </div>
          </div>
          <div class="form-group">
            <label>需求内容 <span class="required">*</span></label>
            <textarea
              v-model="demandForm.requirements_content"
              class="form-textarea"
              rows="4"
              placeholder="详细描述需求内容（至少10个字符）"
            ></textarea>
          </div>
          <div class="form-group">
            <label>目标专业领域</label>
            <div class="checkbox-group">
              <label v-for="major in targetMajorOptions" :key="major" class="checkbox-label">
                <input type="checkbox" :value="major" v-model="demandForm.target_majors" />
                {{ major }}
              </label>
            </div>
          </div>
          <div class="form-group">
            <label>联系方式</label>
            <input v-model="demandForm.contact_info" class="form-input" placeholder="联系电话或邮箱" />
          </div>
          <button class="btn primary" :disabled="submittingDemand" @click="handlePublishDemand">
            <i class="fas fa-paper-plane"></i> {{ submittingDemand ? '发布中...' : '发布需求' }}
          </button>
        </div>
      </div>
    </section>

    <!-- 需求分类 -->
    <section class="section">
      <div class="container">
        <h2 class="section-title">
          <i class="fas fa-th-large"></i> 需求分类
        </h2>
        <div class="demand-card">
          <div class="category-grid">
            <router-link
              v-for="cat in categories"
              :key="cat.name"
              :to="`/category/${cat.name}`"
              class="cat-link"
              :style="{ background: cat.bg, color: cat.color }"
            >
              <i :class="cat.icon"></i>
              <span>{{ cat.name }}</span>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- 团队中心 -->
    <section class="section">
      <div class="container">
        <h2 class="section-title">
          <i class="fas fa-users"></i> 团队中心
        </h2>
        <div class="section-header-row">
          <div class="section-desc">展示已成立的优秀团队，支持招募队友与寻找团队。</div>
          <div class="section-actions">
            <button class="btn secondary" @click="openRecruit">
              <i class="fas fa-bullhorn"></i> 招募队友
            </button>
            <button class="btn primary" @click="openSkillCard">
              <i class="fas fa-id-card"></i> 发布技能卡片
            </button>
          </div>
        </div>

        <div class="teams-grid">
          <div class="team-card" v-for="team in teams" :key="team.name">
            <div class="team-name">{{ team.name }}</div>
            <div class="team-members">
              成员：{{ team.members.map(m => m.major + '（' + m.grade + '）').join('、') }}
            </div>
            <div class="team-skills">
              <span class="skill" v-for="skill in team.skills" :key="skill">{{ skill }}</span>
            </div>
            <div class="team-exp">过往项目数：{{ team.exp }}</div>
            <div class="team-actions">
              <button class="btn secondary" @click="recruit(team.name)">
                <i class="fas fa-handshake"></i> 招募队友
              </button>
              <router-link to="/team" class="btn primary">
                <i class="fas fa-eye"></i> 查看团队
              </router-link>
            </div>
          </div>
        </div>

        <!-- AI 智能组队助手 -->
        <div class="ai-chat-box">
          <div class="ai-header">
            <div class="ai-title">
              <i class="fas fa-robot"></i> 智能组队助手（AI 赋能）
            </div>
            <div class="ai-desc">
              输入项目 ID 或感兴趣的领域，系统将根据技能互补性、空闲时间、过往经验推荐潜在队友。
            </div>
          </div>

          <div class="ai-messages" ref="aiMessagesRef">
            <div
              v-for="(msg, idx) in aiMessages"
              :key="idx"
              class="msg-row"
              :class="msg.role"
            >
              <div class="msg-avatar" v-if="msg.role === 'assistant'">
                <i class="fas fa-robot"></i>
              </div>
              <div class="msg-bubble" :class="msg.role">
                <template v-if="msg.role === 'assistant'">
                  <div
                    v-if="msg.text"
                    class="markdown-content"
                    v-html="renderMarkdown(msg.text)"
                  ></div>
                  <div
                    v-else-if="idx === aiMessages.length - 1 && aiLoading"
                    class="typing-indicator"
                  >
                    <span></span><span></span><span></span>
                  </div>
                </template>
                <template v-else>{{ msg.text }}</template>
              </div>
              <div class="msg-avatar user-avatar" v-if="msg.role === 'user'">
                <i class="fas fa-user"></i>
              </div>
            </div>
          </div>

          <div class="ai-input-row">
            <input
              v-model="userInput"
              placeholder="输入项目ID或关键词，例如：智慧农业"
              class="ai-input"
              @keyup.enter="sendToAI"
              :disabled="aiLoading"
            />
            <button
              class="btn primary send-btn"
              @click="sendToAI"
              :disabled="aiLoading || !userInput.trim()"
            >
              <i class="fas fa-paper-plane"></i>
              {{ aiLoading ? '思考中...' : '发送' }}
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- 培训赋能站 -->
    <section class="section section-alt">
      <div class="container">
        <h2 class="section-title">
          <i class="fas fa-graduation-cap"></i> 培训赋能站
        </h2>
        <div class="section-desc">
          AI 导师、校内导师与企业专家联合出品的系列课程、常见问题与优秀案例库。
        </div>
        <div class="training-grid">
          <div class="course" v-for="course in courses" :key="course.title">
            <div class="course-icon"><i class="fas fa-play-circle"></i></div>
            <div class="course-title">{{ course.title }}</div>
            <div class="course-meta">{{ course.author }} · {{ course.duration }}</div>
            <button class="btn primary">进入课程</button>
          </div>
        </div>
      </div>
    </section>

    <!-- 后端支撑点 -->
    <section class="section">
      <div class="container">
        <h2 class="section-title">
          <i class="fas fa-map-marked-alt"></i> 后端支撑点（线下网络）
        </h2>
        <div class="section-desc">
          可视化地图展示山东大学在各地建立的研究院、技术转移中心、校友会、合作企业等线下实体。
        </div>
        <div class="support-grid">
          <div class="base" v-for="base in bases" :key="base.name">
            <div class="base-icon"><i class="fas fa-building"></i></div>
            <div class="base-name">{{ base.name }}</div>
            <div class="base-focus">聚焦：{{ base.focus }}</div>
            <div class="base-support">支持：{{ base.support }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 行动进行时 -->
    <section class="section section-alt">
      <div class="container">
        <h2 class="section-title">
          <i class="fas fa-running"></i> 行动进行时
        </h2>
        <div class="section-desc">
          通过文字、图片、视频更新进展；系统自动提醒周报与中期检查。
        </div>
        <div class="feed">
          <div class="log" v-for="(log, i) in logs" :key="i">
            <div class="log-header">
              <div class="log-team">{{ log.team }}</div>
              <div class="log-time">{{ log.time }}</div>
            </div>
            <div class="log-text">{{ log.text }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 成果展示 -->
    <section class="section">
      <div class="container">
        <h2 class="section-title">
          <i class="fas fa-trophy"></i> 成果展示
        </h2>
        <div class="section-desc">
          历年优秀项目的报告、代码、演示、论文、专利、媒体报道等。
        </div>
        <div class="gallery">
          <div class="outcome" v-for="outcome in outcomes" :key="outcome.title">
            <div class="outcome-icon"><i class="fas fa-file-alt"></i></div>
            <div class="outcome-title">{{ outcome.title }}</div>
            <div class="outcome-meta">{{ outcome.meta }}</div>
            <a href="#" class="outcome-link" @click.prevent>查看详情 <i class="fas fa-arrow-right"></i></a>
          </div>
        </div>
      </div>
    </section>

    <AppFooter />
  </div>
</template>

<script setup>
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import { ref, reactive, onMounted, onUnmounted, nextTick } from 'vue'
import { chat } from '@/api/ai'
import { createDemand } from '@/api/demands'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const authStore = useAuthStore()

/* ---------- 需求发布表单 ---------- */
const demandForm = reactive({
  org_name: '',
  org_type: '政府机构',
  internship_location: '',
  estimated_time: '',
  requirements_content: '',
  target_majors: [],
  contact_info: ''
})

const targetMajorOptions = [
  '医疗健康', '基础建设', '教育民生', '基层治理', '文旅', '环境'
]

const submittingDemand = ref(false)

const handlePublishDemand = async () => {
  if (!demandForm.org_name || !demandForm.internship_location || !demandForm.requirements_content) {
    ElMessage.warning('请填写必填项')
    return
  }
  if (demandForm.requirements_content.length < 10) {
    ElMessage.warning('需求内容至少10个字符')
    return
  }

  submittingDemand.value = true
  try {
    await createDemand({
      org_name: demandForm.org_name,
      org_type: demandForm.org_type,
      internship_location: demandForm.internship_location,
      estimated_time: demandForm.estimated_time || '面议',
      requirements_content: demandForm.requirements_content,
      target_majors: demandForm.target_majors,
      contact_info: demandForm.contact_info || '待定'
    })
    ElMessage.success('需求发布成功！')
    Object.assign(demandForm, {
      org_name: '', org_type: '政府机构', internship_location: '',
      estimated_time: '', requirements_content: '', target_majors: [], contact_info: ''
    })
  } catch (err) {
    const msg = err.response?.data?.detail || '发布失败，请稍后重试'
    ElMessage.error(msg)
  } finally {
    submittingDemand.value = false
  }
}

/* ---------- 数据看板 ---------- */
const stats = ref([
  { value: 128, label: '已发布需求' },
  { value: 42, label: '成功匹配团队' },
  { value: 18, label: '覆盖省市' },
  { value: 26, label: '专利/论文数量' }
])

/* ---------- 轮播 ---------- */
const slides = [
  { cls: 'one', text: '学生团队在乡村调研 · 数字文旅 · 智慧农业' },
  { cls: 'two', text: '企业导师线上讲座 · 项目孵化' },
  { cls: 'three', text: '技术转移与成果发布 · 专利申请' }
]
const currentSlide = ref(0)
let carouselTimer = null
const nextSlide = () => { currentSlide.value = (currentSlide.value + 1) % slides.length }
const prevSlide = () => { currentSlide.value = (currentSlide.value - 1 + slides.length) % slides.length }
const goToSlide = (i) => { currentSlide.value = i }

/* ---------- 搜索 ---------- */
const searchQuery = ref('')
const handleSearch = () => {
  if (searchQuery.value.trim()) {
    ElMessage.info(`搜索需求：${searchQuery.value}`)
  }
}

/* ---------- 需求分类 ---------- */
const categories = [
  { name: '医疗健康', icon: 'fas fa-heartbeat', bg: 'linear-gradient(135deg, var(--color-primary-light), var(--color-primary-light))', color: 'var(--color-primary)' },
  { name: '基础建设', icon: 'fas fa-hard-hat', bg: 'linear-gradient(135deg, #f0fff4, rgba(47,107,79,.08))', color: 'var(--el-color-success)' },
  { name: '教育民生', icon: 'fas fa-book-reader', bg: 'linear-gradient(135deg, #fff8f0, #fff0e6)', color: 'var(--el-color-warning)' },
  { name: '基层治理', icon: 'fas fa-landmark', bg: 'linear-gradient(135deg, var(--talent-bg), var(--talent-bg))', color: 'var(--talent)' },
  { name: '文旅', icon: 'fas fa-plane-departure', bg: 'linear-gradient(135deg, #fff0f5, var(--color-accent-light))', color: '#16305c' },
  { name: '环境', icon: 'fas fa-leaf', bg: 'linear-gradient(135deg, #f0fff8, #e6fff0)', color: '#2f6b4f' }
]

/* ---------- 团队中心 ---------- */
const teams = ref([
  {
    name: '智农先锋',
    members: [
      { major: '计算机', grade: '2023' },
      { major: '农学', grade: '2022' },
      { major: '市场营销', grade: '2021' }
    ],
    skills: ['Python', '数据分析', '电商'],
    exp: 3
  },
  {
    name: '文旅筑梦',
    members: [
      { major: '设计', grade: '2024' },
      { major: '传媒', grade: '2023' }
    ],
    skills: ['UI/UX', '短视频策划'],
    exp: 2
  },
  {
    name: '医护连心',
    members: [
      { major: '公共卫生', grade: '2022' },
      { major: '软件工程', grade: '2023' }
    ],
    skills: ['后端', '数据可视化'],
    exp: 1
  }
])

const recruit = (name) => {
  ElMessage.success(`向团队【${name}】发起加入申请`)
}
const openRecruit = () => {
  ElMessage.info('打开招募窗口（示意）')
}
const openSkillCard = () => {
  ElMessage.info('发布技能卡片（示意）')
}

/* ---------- 培训赋能站 ---------- */
const courses = [
  { title: '项目管理与进度控制', author: '校内导师', duration: '2h' },
  { title: '乡村调研方法论', author: '企业专家', duration: '1.5h' },
  { title: '数据安全与隐私保护', author: '信息中心', duration: '1h' },
  { title: '孵化与成果转化指南', author: '技术转移中心', duration: '2h' }
]

/* ---------- 后端支撑点 ---------- */
const bases = [
  { name: '烟台研究院', focus: '智慧海洋·海洋经济', support: '办公空间、导师支持' },
  { name: '菏泽校友会', focus: '农业技术推广', support: '渠道对接' },
  { name: '济南技术转移中心', focus: '技术孵化', support: '专利咨询、融资对接' }
]

/* ---------- 实践日志 ---------- */
const logs = [
  { team: '智农先锋', time: '2025-09-01', text: '完成第一轮用户访谈并整理问卷结果，下一步准备数据采集。' },
  { team: '文旅筑梦', time: '2025-08-20', text: '取得地方文化馆合作，开始历史素材数字化采集。' }
]

/* ---------- 成果展示 ---------- */
const outcomes = [
  { title: '农村电商助手 · 项目报告', meta: '软件/演示/论文' },
  { title: '数字文旅样例站点', meta: '网站/演示' },
  { title: '远程诊疗系统调研报告', meta: '报告/调研' }
]

/* ---------- AI 智能组队助手 ---------- */
const aiMessages = ref([
  { role: 'assistant', text: '您好！我是智能组队助手。请输入项目ID或感兴趣的领域（如"智慧农业"），我将为您推荐合适的队友。' }
])
const userInput = ref('')
const aiLoading = ref(false)
const aiMessagesRef = ref(null)

const sendToAI = async () => {
  const input = userInput.value.trim()
  if (!input || aiLoading.value) return

  aiMessages.value.push({ role: 'user', text: input })
  aiMessages.value.push({ role: 'assistant', text: '' })
  const assistantIndex = aiMessages.value.length - 1
  userInput.value = ''
  aiLoading.value = true

  await nextTick()
  scrollToBottom()

  try {
    await chat(input, (chunk) => {
      aiMessages.value[assistantIndex].text += chunk
      scrollToBottom()
    })
  } catch (err) {
    aiMessages.value[assistantIndex].text = '抱歉，请求失败：' + (err.message || '未知错误')
  } finally {
    aiLoading.value = false
  }
}

const scrollToBottom = () => {
  nextTick(() => {
    if (aiMessagesRef.value) {
      aiMessagesRef.value.scrollTop = aiMessagesRef.value.scrollHeight
    }
  })
}

/* ---------- Markdown 解析 ---------- */
function renderMarkdown(text) {
  if (!text) return ''
  let html = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')

  // 代码块
  html = html.replace(/```([\s\S]*?)```/g, (_, code) => `<pre><code>${code.trim()}</code></pre>`)
  // 标题
  html = html.replace(/^###\s+(.*$)/gm, '<h3>$1</h3>')
  html = html.replace(/^##\s+(.*$)/gm, '<h2>$1</h2>')
  html = html.replace(/^#\s+(.*$)/gm, '<h1>$1</h1>')
  // 粗体和斜体
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>')
  // 行内代码
  html = html.replace(/`(.*?)`/g, '<code>$1</code>')
  // 列表项
  html = html.replace(/^[\-\*]\s+(.*$)/gm, '&bull; $1')
  html = html.replace(/^\d+\.\s+(.*$)/gm, (match, p1, offset, str) => {
    const lineStart = str.lastIndexOf('\n', offset) + 1
    const lineNum = str.slice(lineStart, offset).match(/\d+/)
    return `${lineNum ? parseInt(lineNum[0]) + 1 : 1}. $1`
  })
  // 换行
  html = html.replace(/\n/g, '<br>')
  // 清理代码块内的 <br>
  html = html.replace(/<pre><code>([\s\S]*?)<\/code><\/pre>/g, (_, code) => {
    return `<pre><code>${code.replace(/<br>/g, '\n')}</code></pre>`
  })
  return html
}

/* ---------- 生命周期 ---------- */
onMounted(() => {
  carouselTimer = setInterval(nextSlide, 6000)
})
onUnmounted(() => {
  if (carouselTimer) clearInterval(carouselTimer)
})
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: var(--color-bg);
}

/* ---------- Hero ---------- */
.hero-section {
  padding: 30px 5% 40px;
  background: linear-gradient(180deg, var(--color-accent-light), var(--color-bg));
}

.hero-grid {
  display: grid;
  grid-template-columns: 1fr 420px;
  gap: 24px;
  align-items: stretch;
}

.hero-card {
  background: linear-gradient(180deg, rgba(200, 16, 46, 0.05), transparent);
  padding: 30px;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
}

.hero-card h1 {
  color: var(--color-primary-dark);
  margin: 0 0 8px;
  font-size: 28px;
}

.hero-desc {
  margin: 0 0 18px;
  color: var(--color-text-muted);
  font-size: 14px;
}

.cta-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

/* ---------- 按钮 ---------- */
.btn {
  padding: 12px 16px;
  border-radius: var(--radius-sm);
  border: 0;
  cursor: pointer;
  font-weight: 600;
  font-size: 15px;
  font-family: var(--font-family);
  display: inline-flex;
  align-items: center;
  gap: 6px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn.primary {
  background: var(--color-primary);
  color: white;
}

.btn.primary:hover {
  background: var(--color-primary-dark);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.btn.primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn.secondary {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  color: var(--color-text);
}

.btn.secondary:hover {
  background: var(--color-bg-alt);
}

.btn.icon-btn {
  padding: 12px 14px;
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  color: var(--color-text-light);
}

.btn.icon-btn:hover {
  background: var(--color-bg-alt);
  color: var(--color-primary);
}

/* ---------- 数据看板 ---------- */
.board {
  display: flex;
  gap: 12px;
  margin-top: 18px;
}

.stat {
  flex: 1;
  background: var(--color-bg-card);
  padding: 14px;
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
}

.stat .num {
  font-size: 22px;
  color: var(--color-primary-dark);
  font-weight: 800;
}

.stat .label {
  color: var(--color-text-muted);
  font-size: 13px;
  margin-top: 2px;
}

/* ---------- 轮播 ---------- */
.hero-right {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.carousel {
  position: relative;
  border-radius: var(--radius-sm);
  overflow: hidden;
  height: 260px;
  box-shadow: var(--shadow-md);
}

.slide {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: #fff;
  font-weight: 700;
  text-align: center;
  padding: 20px;
  transition: transform 0.5s ease;
}

.slide.one {
  background: linear-gradient(135deg, var(--color-primary-dark), var(--color-accent));
}

.slide.two {
  background: linear-gradient(135deg, var(--color-accent), var(--color-primary-dark));
}

.slide.three {
  background: linear-gradient(135deg, var(--el-color-success), #2f6b4f);
}

.dots {
  position: absolute;
  right: 12px;
  bottom: 12px;
  display: flex;
  gap: 8px;
}

.dot {
  width: 10px;
  height: 10px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 50%;
  cursor: pointer;
  transition: background 0.2s;
}

.dot.active {
  background: white;
}

.search-row {
  display: flex;
  gap: 8px;
  align-items: center;
}

.search-input {
  flex: 1;
  padding: 10px 14px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border);
  font-size: 14px;
  font-family: var(--font-family);
  outline: none;
  transition: border-color 0.2s;
}

.search-input:focus {
  border-color: var(--color-accent);
}

/* ---------- 通用区块 ---------- */
.section {
  padding: 36px 5%;
}

.section-alt {
  background-color: var(--color-bg-alt);
}

.section-title {
  font-size: 24px;
  color: var(--color-accent-dark);
  margin: 0 0 16px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-title i {
  color: var(--color-primary-dark);
}

.section-desc {
  color: var(--color-text-muted);
  font-size: 14px;
  margin-bottom: 16px;
}

.section-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.section-actions {
  display: flex;
  gap: 8px;
}

/* ---------- 需求分类 ---------- */
.demand-card {
  background: var(--color-bg-card);
  padding: 24px;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
}

.cat-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 20px 16px;
  border-radius: var(--radius-sm);
  text-decoration: none;
  font-weight: 600;
  text-align: center;
  transition: transform 0.2s, box-shadow 0.2s;
}

.cat-link:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}

.cat-link i {
  font-size: 28px;
}

.cat-link span {
  font-size: 16px;
}

/* ---------- 团队卡片 ---------- */
.teams-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.team-card {
  background: var(--color-bg-card);
  padding: 16px;
  border-radius: var(--radius-sm);
  width: 280px;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s, box-shadow 0.2s;
}

.team-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}

.team-name {
  font-weight: 800;
  font-size: 18px;
  color: var(--color-accent-dark);
}

.team-members {
  font-size: 13px;
  color: var(--color-text-muted);
  margin-top: 6px;
}

.team-skills {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.skill {
  display: inline-block;
  padding: 4px 10px;
  border-radius: var(--radius-sm);
  background: var(--color-accent-light);
  color: var(--color-accent-dark);
  font-size: 12px;
}

.team-exp {
  margin-top: 8px;
  color: var(--color-text-muted);
  font-size: 13px;
}

.team-actions {
  margin-top: 12px;
  display: flex;
  gap: 8px;
}

.team-actions .btn {
  flex: 1;
  justify-content: center;
  font-size: 14px;
  padding: 8px 12px;
}

/* ---------- AI 聊天 ---------- */
.ai-chat-box {
  margin-top: 20px;
  background: linear-gradient(90deg, var(--color-bg-card), #fffdf5);
  padding: 20px;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--color-border);
}

.ai-header {
  margin-bottom: 16px;
}

.ai-title {
  font-weight: 700;
  font-size: 18px;
  color: var(--color-accent-dark);
  display: flex;
  align-items: center;
  gap: 8px;
}

.ai-title i {
  color: var(--color-accent);
}

.ai-desc {
  color: var(--color-text-muted);
  font-size: 13px;
  margin-top: 6px;
}

.ai-messages {
  background: var(--color-bg-alt);
  border-radius: var(--radius-sm);
  padding: 16px;
  max-height: 400px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.msg-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.msg-row.user {
  flex-direction: row-reverse;
}

.msg-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 16px;
}

.msg-row.assistant .msg-avatar {
  background: linear-gradient(135deg, var(--color-accent), var(--color-accent-dark));
  color: white;
}

.msg-avatar.user-avatar {
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  color: white;
}

.msg-bubble {
  max-width: 75%;
  padding: 12px 16px;
  border-radius: var(--radius-md);
  font-size: 14px;
  line-height: 1.6;
  word-break: break-word;
}

.msg-bubble.assistant {
  background: var(--color-bg-card);
  color: var(--color-text);
  border: 1px solid var(--color-border);
  border-top-left-radius: 4px;
}

.msg-bubble.user {
  background: var(--color-primary);
  color: white;
  border-top-right-radius: 4px;
}

/* 打字动画 */
.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 4px 0;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-text-muted);
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% { opacity: 0.3; transform: scale(0.8); }
  30% { opacity: 1; transform: scale(1); }
}

.ai-input-row {
  margin-top: 14px;
  display: flex;
  gap: 8px;
  align-items: center;
}

.ai-input {
  flex: 1;
  padding: 12px 16px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border);
  font-size: 14px;
  font-family: var(--font-family);
  outline: none;
  transition: border-color 0.2s;
}

.ai-input:focus {
  border-color: var(--color-accent);
}

.ai-input:disabled {
  background: var(--color-bg-alt);
  cursor: not-allowed;
}

.send-btn {
  white-space: nowrap;
}

/* Markdown 内容样式 */
.ai-messages :deep(.markdown-content h1) {
  font-size: 1.5em;
  font-weight: bold;
  margin: 10px 0 8px;
}

.ai-messages :deep(.markdown-content h2) {
  font-size: 1.3em;
  font-weight: bold;
  margin: 10px 0 8px;
}

.ai-messages :deep(.markdown-content h3) {
  font-size: 1.1em;
  font-weight: bold;
  margin: 8px 0 6px;
}

.ai-messages :deep(.markdown-content p) {
  margin: 6px 0;
}

.ai-messages :deep(.markdown-content strong) {
  font-weight: bold;
}

.ai-messages :deep(.markdown-content em) {
  font-style: italic;
}

.ai-messages :deep(.markdown-content code) {
  font-family: monospace;
  background: var(--color-bg-alt);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.9em;
}

.ai-messages :deep(.markdown-content pre) {
  background: var(--color-accent-dark);
  color: #e8e8e8;
  padding: 12px;
  border-radius: var(--radius-sm);
  overflow-x: auto;
  margin: 8px 0;
}

.ai-messages :deep(.markdown-content pre code) {
  background: none;
  padding: 0;
  color: inherit;
}

.ai-messages :deep(.markdown-content ul),
.ai-messages :deep(.markdown-content ol) {
  padding-left: 1.5em;
  margin: 8px 0;
}

.ai-messages :deep(.markdown-content li) {
  margin-bottom: 4px;
}

/* ---------- 培训赋能站 ---------- */
.training-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}

.course {
  background: linear-gradient(180deg, var(--color-bg-card), #fbfbff);
  padding: 18px;
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s, box-shadow 0.2s;
}

.course:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}

.course-icon {
  font-size: 28px;
  color: var(--color-accent);
  margin-bottom: 10px;
}

.course-title {
  font-weight: 700;
  font-size: 16px;
  color: var(--color-accent-dark);
}

.course-meta {
  color: var(--color-text-muted);
  font-size: 13px;
  margin-top: 6px;
  margin-bottom: 12px;
}

/* ---------- 后端支撑点 ---------- */
.support-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}

.base {
  background: var(--color-bg-card);
  padding: 18px;
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-sm);
  border-top: 4px solid var(--color-accent);
  transition: transform 0.2s, box-shadow 0.2s;
}

.base:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}

.base-icon {
  font-size: 24px;
  color: var(--color-accent);
  margin-bottom: 8px;
}

.base-name {
  font-weight: 700;
  font-size: 16px;
  color: var(--color-accent-dark);
}

.base-focus {
  color: var(--color-text-muted);
  font-size: 13px;
  margin-top: 6px;
}

.base-support {
  margin-top: 6px;
  font-size: 14px;
  color: var(--color-text-light);
}

/* ---------- 实践日志 ---------- */
.feed {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.log {
  background: var(--color-bg-card);
  padding: 16px;
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-sm);
  border-left: 4px solid var(--color-primary);
}

.log-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.log-team {
  font-weight: 700;
  color: var(--color-accent-dark);
}

.log-time {
  font-size: 12px;
  color: var(--color-text-muted);
}

.log-text {
  margin-top: 4px;
  color: var(--color-text-light);
  line-height: 1.6;
}

/* ---------- 成果展示 ---------- */
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}

.outcome {
  background: var(--color-bg-card);
  padding: 18px;
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s, box-shadow 0.2s;
}

.outcome:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}

.outcome-icon {
  font-size: 28px;
  color: var(--color-primary);
  margin-bottom: 10px;
}

.outcome-title {
  font-weight: 700;
  font-size: 16px;
  color: var(--color-accent-dark);
}

.outcome-meta {
  color: var(--color-text-muted);
  font-size: 13px;
  margin-top: 6px;
  margin-bottom: 12px;
}

.outcome-link {
  color: var(--color-link);
  font-size: 14px;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: gap 0.2s;
}

.outcome-link:hover {
  gap: 8px;
}

/* ---------- 需求发布表单 ---------- */
.demand-form-card {
  background: var(--color-bg-card);
  padding: 24px;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
}

.form-row {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.form-row .form-group {
  flex: 1;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 6px;
}

.required {
  color: var(--color-primary);
}

.form-input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-family: var(--font-family);
  outline: none;
  transition: border-color 0.2s;
  background: var(--color-bg);
}

.form-input:focus {
  border-color: var(--color-accent);
}

.form-textarea {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-family: var(--font-family);
  outline: none;
  transition: border-color 0.2s;
  resize: vertical;
  background: var(--color-bg);
}

.form-textarea:focus {
  border-color: var(--color-accent);
}

.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  cursor: pointer;
  color: var(--color-text-light);
}

.checkbox-label input {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

/* ---------- 响应式 ---------- */
@media (max-width: 900px) {
  .hero-grid {
    grid-template-columns: 1fr;
  }

  .board {
    flex-wrap: wrap;
  }

  .stat {
    min-width: 120px;
  }

  .teams-grid {
    flex-direction: column;
  }

  .team-card {
    width: 100%;
  }

  .section-header-row {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 600px) {
  .cta-row {
    flex-direction: column;
  }

  .cta-row .btn {
    width: 100%;
    justify-content: center;
  }

  .board {
    flex-direction: column;
  }

  .msg-bubble {
    max-width: 85%;
  }
}
</style>
