<template>
  <div class="comprehensive-page">
    <AppHeader />

    <div class="container">
      <!-- HERO -->
      <div class="hero">
        <div class="hero-card">
          <h1>连接地方需求，赋能学生实践——山大实践一体化平台</h1>
          <p>索引栏直观展示"需求洞察 → 项目匹配 → 赋能培训 → 实地实践 → 成果转化"的全流程，帮助地方单位与学生团队高效协作并实现成果落地。</p>
          <div class="cta-row">
            <router-link to="/register/enterprise" class="btn primary">发布需求（地方/企业）</router-link>
            <router-link to="/register/personal" class="btn primary">发布招募（队长）</router-link>
            <router-link to="/team" class="btn secondary">加入队伍</router-link>
          </div>

          <div class="board-wrapper">
            <div class="board-label">快速数据看板</div>
            <div class="board">
              <div class="stat"><div class="num">{{ stats.posts }}</div><div class="label">已发布需求</div></div>
              <div class="stat"><div class="num">{{ stats.matches }}</div><div class="label">成功匹配团队</div></div>
              <div class="stat"><div class="num">{{ stats.regions }}</div><div class="label">覆盖省市</div></div>
              <div class="stat"><div class="num">{{ stats.results }}</div><div class="label">专利/论文数量</div></div>
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
            >{{ slide.text }}</div>
            <div class="dots">
              <div
                v-for="(slide, i) in slides"
                :key="i"
                class="dot"
                :class="{ active: currentSlide === i }"
                @click="currentSlide = i"
              ></div>
            </div>
          </div>

          <div class="search-row">
            <button class="btn" @click="prevSlide">◀</button>
            <button class="btn" @click="nextSlide">▶</button>
            <div class="search-spacer"></div>
            <input v-model="searchQuery" placeholder="按项目/地区/类型搜索需求" class="search-input" />
          </div>
        </div>
      </div>

      <!-- 需求库 -->
      <section id="demand">
        <h2 class="section-title">需求库</h2>
        <div class="demand">
          <div class="map">
            <div class="map-hint">中国地图 · 点击省份查看需求</div>
            <div class="map-area">
              <div class="map-placeholder">
                <i class="fas fa-map-marked-alt"></i>
                <p>地图区域</p>
                <p class="map-sub">点击红色标记查看需求详情</p>
              </div>
              <div
                v-for="(p, i) in filteredProjects"
                :key="p.id"
                class="map-dot"
                :style="{
                  left: 10 + (i * 18) % 80 + '%',
                  top: 10 + (i * 22) % 70 + '%'
                }"
                :title="p.title"
                @click="selectedProject = p"
              ></div>
            </div>
          </div>

          <div class="project-list">
            <div
              v-for="p in filteredProjects"
              :key="p.id"
              class="project-card"
              @click="selectedProject = p"
            >
              <div class="project-top">
                <div class="project-name">{{ p.title }}</div>
                <div class="project-id">ID: {{ p.id }}</div>
              </div>
              <div class="project-bottom">
                <div class="meta">
                  <span class="tag">{{ p.type }}</span>
                  <span class="unit">{{ p.unit }}</span>
                </div>
                <div class="project-right">
                  <div class="region">{{ p.region }}</div>
                  <div class="urgent"><strong>{{ p.urgent }}</strong> · {{ p.period }}</div>
                </div>
              </div>
            </div>
            <div v-if="filteredProjects.length === 0" class="no-result">未找到匹配的需求</div>
          </div>
        </div>
      </section>

      <!-- 团队中心 -->
      <section id="team">
        <h2 class="section-title">团队中心</h2>
        <div class="section-bar">
          <div class="section-desc">展示已成立的优秀实践团队，支持招募队友与寻找团队。</div>
          <div class="bar-actions">
            <router-link to="/register/personal" class="btn secondary">招募队友</router-link>
            <router-link to="/register/personal" class="btn primary">发布技能卡片</router-link>
          </div>
        </div>
        <div class="teams">
          <div v-for="t in teams" :key="t.name" class="team-card">
            <div class="team-name">{{ t.name }}</div>
            <div class="team-members">成员：{{ t.members.map(m => m.major + '（' + m.grade + '）').join('、') }}</div>
            <div class="skills">
              <span v-for="s in t.skills" :key="s" class="skill">{{ s }}</span>
            </div>
            <div class="team-exp">过往项目数：{{ t.exp }}</div>
            <div class="team-btns">
              <router-link to="/team" class="btn secondary">招募队友</router-link>
              <router-link to="/team" class="btn primary">查看团队</router-link>
            </div>
          </div>
        </div>

        <div class="ai-box">
          <div class="ai-title">智能组队助手（AI 赋能）</div>
          <div class="ai-desc">输入项目 ID 或感兴趣的领域，系统将根据技能互补性、空闲时间、过往经验推荐潜在队友。</div>
          <div class="ai-input-row">
            <input v-model="aiInput" placeholder="输入项目ID或关键词，例如：智慧农业" class="ai-input" @keyup.enter="aiMatch" />
            <button class="btn primary" :disabled="aiLoading" @click="aiMatch">
              {{ aiLoading ? '推荐中...' : 'AI 推荐' }}
            </button>
          </div>
          <div v-if="aiResult" class="ai-answer">
            <div class="ai-result-text" v-html="aiResult"></div>
          </div>
        </div>
      </section>

      <!-- 培训赋能站 -->
      <section id="train">
        <h2 class="section-title">培训赋能站</h2>
        <div class="section-desc">AI 导师、校内导师与企业专家联合出品的系列课程、常见问题与优秀案例库。</div>
        <div class="training-grid">
          <div v-for="c in courses" :key="c.title" class="course">
            <div class="course-title">{{ c.title }}</div>
            <div class="course-meta">{{ c.author }} · {{ c.duration }}</div>
            <button class="btn primary">进入课程</button>
          </div>
        </div>
      </section>

      <!-- 后端支撑点 -->
      <section id="support">
        <h2 class="section-title">后端支撑点（线下网络）</h2>
        <div class="section-desc">可视化地图展示山东大学在各地建立的研究院、技术转移中心、校友会、合作企业等线下实体。</div>
        <div class="support-grid">
          <div v-for="b in bases" :key="b.name" class="base">
            <div class="base-name">{{ b.name }}</div>
            <div class="base-focus">聚焦：{{ b.focus }}</div>
            <div class="base-support">支持：{{ b.support }}</div>
          </div>
        </div>
      </section>

      <!-- 实践进行时 -->
      <section id="practice">
        <h2 class="section-title">实践进行时 · 团队日志</h2>
        <div class="section-desc">团队通过文字、图片、视频更新进展；系统自动提醒周报与中期检查。</div>
        <div class="feed">
          <div v-for="l in logs" :key="l.team + l.time" class="log">
            <div class="log-team">{{ l.team }}</div>
            <div class="log-time">{{ l.time }}</div>
            <div class="log-text">{{ l.text }}</div>
          </div>
        </div>
      </section>

      <!-- 成果展示 -->
      <section id="results">
        <h2 class="section-title">成果展示</h2>
        <div class="section-desc">历年优秀实践项目的报告、代码、演示、论文、专利、媒体报道等。</div>
        <div class="gallery">
          <div v-for="o in outcomes" :key="o.title" class="outcome">
            <div class="outcome-title">{{ o.title }}</div>
            <div class="outcome-meta">{{ o.meta }}</div>
            <router-link to="/achievement" class="outcome-link">查看详情</router-link>
          </div>
        </div>
      </section>

      <footer class="page-footer">
        © 2025 山东大学 · 鸿雁服务平台 · 本页面为原型样例，不含真实数据
      </footer>
    </div>

    <!-- 需求详情弹窗 -->
    <div v-if="selectedProject" class="modal-overlay" @click.self="selectedProject = null">
      <div class="modal-card">
        <button class="modal-close" @click="selectedProject = null"><i class="fas fa-times"></i></button>
        <h3>{{ selectedProject.title }}</h3>
        <div class="modal-meta">
          <span class="tag">{{ selectedProject.type }}</span>
          <span>{{ selectedProject.region }}</span>
          <span>{{ selectedProject.unit }}</span>
        </div>
        <div class="modal-info">
          <div>紧急度：<strong>{{ selectedProject.urgent }}</strong></div>
          <div>周期：{{ selectedProject.period }}</div>
          <div>项目 ID：{{ selectedProject.id }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import AppHeader from '@/components/layout/AppHeader.vue'

const stats = ref({ posts: 128, matches: 42, regions: 18, results: 26 })

const projects = ref([
  { id: 'P-001', title: 'XX县农产品电商直播智能助手开发', unit: '泰安市XX县农业局', region: '山东·泰安', type: '智慧农业', urgent: '高', period: '3个月' },
  { id: 'P-002', title: '海滨小镇数字文旅内容策划', unit: '青岛市文化和旅游局', region: '山东·青岛', type: '数字文旅', urgent: '中', period: '4个月' },
  { id: 'P-003', title: '基层卫生站远程诊疗系统需求调研', unit: '临沂市某卫生服务中心', region: '山东·临沂', type: '智慧医疗', urgent: '高', period: '6个月' },
  { id: 'P-004', title: '乡村太阳能微电网优化方案', unit: '德州市能源办', region: '山东·德州', type: '新能源', urgent: '低', period: '5个月' },
  { id: 'P-005', title: '地方非遗文化数据库建设', unit: '济宁市文化馆', region: '山东·济宁', type: '数字文旅', urgent: '中', period: '4个月' },
])

const teams = ref([
  { name: '智农先锋', members: [{ major: '计算机', grade: '2023' }, { major: '农学', grade: '2022' }, { major: '市场营销', grade: '2021' }], skills: ['Python', '数据分析', '电商'], exp: 3 },
  { name: '文旅筑梦', members: [{ major: '设计', grade: '2024' }, { major: '传媒', grade: '2023' }], skills: ['UI/UX', '短视频策划'], exp: 2 },
  { name: '医护连心', members: [{ major: '公共卫生', grade: '2022' }, { major: '软件工程', grade: '2023' }], skills: ['后端', '数据可视化'], exp: 1 },
])

const courses = ref([
  { title: '项目管理与进度控制', author: '校内导师', duration: '2h' },
  { title: '乡村调研方法论', author: '企业专家', duration: '1.5h' },
  { title: '数据安全与隐私保护', author: '信息中心', duration: '1h' },
  { title: '孵化与成果转化指南', author: '技术转移中心', duration: '2h' },
])

const bases = ref([
  { name: '烟台研究院', focus: '智慧海洋·海洋经济', support: '办公空间、导师支持' },
  { name: '菏泽校友会', focus: '农业技术推广', support: '渠道对接' },
  { name: '济南技术转移中心', focus: '技术孵化', support: '专利咨询、融资对接' },
])

const logs = ref([
  { team: '智农先锋', time: '2025-09-01', text: '完成第一轮用户访谈并整理问卷结果，下一步准备数据采集。' },
  { team: '文旅筑梦', time: '2025-08-20', text: '取得地方文化馆合作，开始历史素材数字化采集。' },
])

const outcomes = ref([
  { title: '农村电商助手 · 项目报告', meta: '软件/演示/论文', link: '#' },
  { title: '数字文旅样例站点', meta: '网站/演示', link: '#' },
  { title: '远程诊疗系统调研报告', meta: '报告/调研', link: '#' },
])

const slides = [
  { text: '学生团队在乡村调研 · 数字文旅 · 智慧农业', cls: 'one' },
  { text: '企业导师线上讲座 · 项目孵化', cls: 'two' },
  { text: '技术转移与成果发布 · 专利申请', cls: 'three' },
]

const currentSlide = ref(0)
let carouselTimer = null
const searchQuery = ref('')
const selectedProject = ref(null)
const aiInput = ref('')
const aiResult = ref('')
const aiLoading = ref(false)

const filteredProjects = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return projects.value
  return projects.value.filter(p =>
    (p.title + p.unit + p.region + p.type).toLowerCase().includes(q)
  )
})

const nextSlide = () => { currentSlide.value = (currentSlide.value + 1) % slides.length }
const prevSlide = () => { currentSlide.value = (currentSlide.value - 1 + slides.length) % slides.length }

const aiMatch = () => {
  if (!aiInput.value.trim()) return
  aiLoading.value = true
  aiResult.value = ''
  setTimeout(() => {
    aiResult.value = `<p>根据您输入的关键词「${aiInput.value}」，系统推荐以下方向：</p><ul><li>可关注<strong>智慧农业</strong>相关项目，匹配团队「智农先锋」</li><li>建议补充技能：<code>Python</code>、<code>数据分析</code></li><li>推荐课程：乡村调研方法论（1.5h）</li></ul>`
    aiLoading.value = false
  }, 1500)
}

onMounted(() => {
  carouselTimer = setInterval(nextSlide, 6000)
})
onUnmounted(() => {
  if (carouselTimer) clearInterval(carouselTimer)
})
</script>

<style scoped>
.comprehensive-page {
  background: #f8f8f9;
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 28px auto;
  padding: 0 20px;
}

/* HERO */
.hero {
  display: grid;
  grid-template-columns: 1fr 420px;
  gap: 20px;
  align-items: center;
  margin-top: 8px;
}

.hero-card {
  background: linear-gradient(180deg, rgba(200, 16, 46, 0.05), transparent);
  padding: 28px;
  border-radius: 12px;
  box-shadow: 0 6px 18px rgba(30, 30, 30, 0.08);
}

.hero-card h1 {
  color: #16305c;
  margin: 0 0 8px;
  font-size: 28px;
}

.hero-card p {
  margin: 0 0 18px;
  color: #6b6b6b;
  line-height: 1.6;
}

.cta-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.btn {
  padding: 12px 16px;
  border-radius: 10px;
  border: 0;
  cursor: pointer;
  font-weight: 600;
  text-decoration: none;
  display: inline-block;
  text-align: center;
  font-size: 14px;
  transition: opacity 0.2s;
}

.btn:hover { opacity: 0.85; }
.btn.primary { background: #16305c; color: white; }
.btn.secondary { background: white; border: 1px solid #e6e6e6; color: #333; }

.board-wrapper { margin-top: 18px; }
.board-label { font-size: 13px; color: #6b6b6b; margin-bottom: 8px; }

.board {
  display: flex;
  gap: 12px;
}

.stat {
  flex: 1;
  background: #fff;
  padding: 14px;
  border-radius: 10px;
  box-shadow: 0 6px 18px rgba(30, 30, 30, 0.08);
  display: flex;
  flex-direction: column;
}

.stat .num { font-size: 20px; color: #16305c; font-weight: 800; }
.stat .label { color: #6b6b6b; font-size: 13px; }

.hero-right { display: flex; flex-direction: column; gap: 12px; }

.carousel {
  position: relative;
  border-radius: 10px;
  overflow: hidden;
  height: 260px;
  background: linear-gradient(90deg, #fff, #fafafa);
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
  transition: transform 0.5s ease;
  padding: 20px;
  text-align: center;
}

.slide.one { background: linear-gradient(135deg, #16305c, var(--color-accent)); }
.slide.two { background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark)); }
.slide.three { background: linear-gradient(135deg, var(--el-color-success), #2f6b4f); }

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
  transition: all 0.3s;
}

.dot.active { background: #fff; transform: scale(1.3); }

.search-row {
  display: flex;
  gap: 8px;
  align-items: center;
}

.search-spacer { flex: 1; }

.search-input {
  padding: 10px;
  border-radius: 10px;
  border: 1px solid #eee;
  width: 62%;
  font-size: 14px;
}

/* SECTIONS */
section { margin-top: 28px; }

.section-title {
  margin: 0 0 12px;
  color: #222;
  font-size: 22px;
  font-weight: 700;
}

.section-desc {
  color: #6b6b6b;
  font-size: 14px;
  margin-bottom: 8px;
}

/* 需求库 */
.demand {
  display: flex;
  gap: 18px;
}

.map {
  flex: 1;
  background: #fff;
  padding: 12px;
  border-radius: 10px;
  box-shadow: 0 6px 18px rgba(30, 30, 30, 0.08);
  min-height: 380px;
}

.map-hint {
  font-size: 13px;
  color: #6b6b6b;
  margin-bottom: 8px;
}

.map-area {
  position: relative;
  width: 100%;
  height: 320px;
  background: var(--paper-2);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.map-placeholder {
  text-align: center;
  color: #999;
}

.map-placeholder i {
  font-size: 48px;
  color: #ccc;
  margin-bottom: 8px;
}

.map-placeholder p {
  font-size: 14px;
  margin: 2px 0;
}

.map-sub {
  font-size: 12px !important;
  color: #bbb !important;
}

.map-dot {
  position: absolute;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #16305c;
  cursor: pointer;
  box-shadow: 0 0 8px rgba(200, 16, 46, 0.6);
  transition: transform 0.2s;
}

.map-dot:hover { transform: scale(1.5); }

.project-list {
  width: 480px;
  background: #fff;
  padding: 12px;
  border-radius: 10px;
  box-shadow: 0 6px 18px rgba(30, 30, 30, 0.08);
  overflow: auto;
  max-height: 520px;
}

.project-card {
  border-radius: 10px;
  padding: 12px;
  margin-bottom: 10px;
  border: 1px solid #f0f0f0;
  cursor: pointer;
  transition: box-shadow 0.2s;
}

.project-card:hover { box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); }

.project-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.project-name { font-weight: 700; font-size: 14px; }
.project-id { font-size: 13px; color: #6b6b6b; }

.project-bottom {
  margin-top: 8px;
  display: flex;
  justify-content: space-between;
}

.meta {
  display: flex;
  gap: 8px;
  align-items: center;
  font-size: 13px;
  color: #6b6b6b;
}

.tag {
  background: #f3f3f3;
  padding: 4px 8px;
  border-radius: 8px;
  font-size: 12px;
}

.unit { margin-left: 8px; }

.project-right {
  text-align: right;
  min-width: 140px;
}

.region { font-size: 13px; color: #6b6b6b; }
.urgent { margin-top: 6px; font-size: 13px; }

.no-result {
  text-align: center;
  padding: 30px;
  color: #999;
}

/* 团队中心 */
.section-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.bar-actions { display: flex; gap: 8px; }

.teams {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 12px;
}

.team-card {
  background: #fff;
  padding: 12px;
  border-radius: 10px;
  width: 240px;
  box-shadow: 0 6px 18px rgba(30, 30, 30, 0.08);
}

.team-name { font-weight: 800; font-size: 16px; }
.team-members { font-size: 13px; color: #6b6b6b; margin-top: 6px; }

.skills { margin-top: 8px; }

.skill {
  display: inline-block;
  padding: 6px 8px;
  border-radius: 8px;
  margin: 6px 6px 0 0;
  background: #f5f5f5;
  font-size: 12px;
}

.team-exp {
  margin-top: 8px;
  color: #6b6b6b;
  font-size: 13px;
}

.team-btns {
  margin-top: 8px;
  display: flex;
  gap: 8px;
}

.ai-box {
  margin-top: 12px;
  background: linear-gradient(90deg, #fff, #fffdf5);
  padding: 12px;
  border-radius: 10px;
  box-shadow: 0 6px 18px rgba(30, 30, 30, 0.08);
}

.ai-title { font-weight: 700; font-size: 16px; }
.ai-desc { color: #6b6b6b; font-size: 13px; margin-top: 6px; }

.ai-input-row {
  margin-top: 10px;
  display: flex;
  gap: 8px;
  align-items: center;
}

.ai-input {
  padding: 10px;
  border-radius: 10px;
  border: 1px solid #eee;
  flex: 1;
  font-size: 14px;
}

.ai-answer {
  background: #fff;
  padding: 12px;
  border-radius: 12px;
  margin-top: 10px;
  max-height: 300px;
  overflow-y: auto;
}

.ai-result-text :deep(p) { margin: 8px 0; line-height: 1.6; }
.ai-result-text :deep(ul) { padding-left: 2em; margin: 8px 0; }
.ai-result-text :deep(li) { margin-bottom: 4px; }
.ai-result-text :deep(strong) { font-weight: bold; }
.ai-result-text :deep(code) { background: #f4f4f4; padding: 2px 4px; border-radius: 3px; font-family: monospace; }

/* 培训赋能站 */
.training-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 12px;
}

.course {
  background: linear-gradient(180deg, #fff, #fbfbff);
  padding: 16px;
  border-radius: 10px;
  box-shadow: 0 6px 18px rgba(30, 30, 30, 0.08);
  text-align: center;
}

.course-title { font-weight: 700; font-size: 15px; }
.course-meta { color: #6b6b6b; font-size: 13px; margin-top: 6px; margin-bottom: 10px; }

/* 后端支撑点 */
.support-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.base {
  background: #fff;
  padding: 16px;
  border-radius: 10px;
  box-shadow: 0 6px 18px rgba(30, 30, 30, 0.08);
}

.base-name { font-weight: 700; font-size: 15px; }
.base-focus { color: #6b6b6b; font-size: 13px; margin-top: 6px; }
.base-support { margin-top: 4px; font-size: 13px; }

/* 实践进行时 */
.feed {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.log {
  background: #fff;
  padding: 14px;
  border-radius: 10px;
  box-shadow: 0 6px 18px rgba(30, 30, 30, 0.08);
}

.log-team { font-weight: 700; font-size: 15px; }
.log-time { font-size: 12px; color: #6b6b6b; }
.log-text { margin-top: 8px; line-height: 1.6; }

/* 成果展示 */
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 12px;
}

.outcome {
  background: #fff;
  padding: 16px;
  border-radius: 10px;
  box-shadow: 0 6px 18px rgba(30, 30, 30, 0.08);
}

.outcome-title { font-weight: 700; font-size: 15px; }
.outcome-meta { color: #6b6b6b; font-size: 13px; margin-top: 6px; margin-bottom: 10px; }
.outcome-link { color: #16305c; text-decoration: none; font-size: 14px; font-weight: 600; }
.outcome-link:hover { text-decoration: underline; }

/* 页脚 */
.page-footer {
  margin: 32px 0 80px;
  color: #6b6b6b;
  text-align: center;
  font-size: 13px;
}

/* 弹窗 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-card {
  background: #fff;
  padding: 30px;
  border-radius: 12px;
  max-width: 500px;
  width: 90%;
  position: relative;
}

.modal-close {
  position: absolute;
  top: 12px;
  right: 12px;
  border: none;
  background: #f0f0f0;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  color: #666;
}

.modal-card h3 { margin: 0 0 16px; font-size: 20px; }

.modal-meta {
  display: flex;
  gap: 10px;
  align-items: center;
  font-size: 14px;
  color: #6b6b6b;
  margin-bottom: 16px;
}

.modal-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 14px;
  line-height: 1.6;
}

/* 响应式 */
@media (max-width: 900px) {
  .hero { grid-template-columns: 1fr; }
  .demand { flex-direction: column; }
  .project-list { width: 100%; max-height: 400px; }
}
</style>
