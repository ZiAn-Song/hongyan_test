<template>
  <div class="page">
    <AppHeader />

    <div class="forum-page">
      <!-- 论坛标题区 -->
      <div class="forum-header">
        <div class="forum-title-wrap">
          <h1 class="forum-title">万里边疆 - 实时论坛</h1>
          <p class="forum-subtitle">连接边疆实践，分享真知灼见</p>
        </div>
        <router-link to="/publish" class="new-post-btn">
          <i class="fas fa-edit"></i>
          <span>发布话题</span>
        </router-link>
      </div>

      <!-- 论坛主体布局 -->
      <div class="forum-container">
        <!-- 左侧帖子列表 -->
        <div class="left-content">
          <!-- 排序标签 -->
          <div class="content-tabs">
            <div
              class="content-tab"
              :class="{ active: activeTab === 'hot' }"
              @click="switchTab('hot')"
            >
              <i class="fas fa-fire"></i>
              热门
            </div>
            <div
              class="content-tab"
              :class="{ active: activeTab === 'new' }"
              @click="switchTab('new')"
            >
              <i class="fas fa-clock"></i>
              最新
            </div>
          </div>

          <!-- 帖子卡片列表 -->
          <div class="post-list">
            <router-link
              v-for="post in filteredPosts"
              :key="post.id"
              :to="'/forum/' + post.id"
              class="post-card"
            >
              <!-- 作者信息 -->
              <div class="author-info">
                <div class="author-avatar">
                  <i class="fas fa-user-circle"></i>
                </div>
                <div class="author-details">
                  <div class="author-name">{{ post.author }}</div>
                  <div class="author-meta">
                    <span class="meta-item">
                      <i class="far fa-clock"></i>
                      {{ post.date }}
                    </span>
                    <span class="meta-item">
                      <i class="fas fa-users"></i>
                      {{ post.team }}
                    </span>
                    <span class="meta-item">
                      <i class="fas fa-map-marker-alt"></i>
                      {{ post.location }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- 帖子标题 -->
              <h2 class="post-title">{{ post.title }}</h2>

              <!-- 帖子摘要 -->
              <p class="post-summary">{{ post.summary }}</p>

              <!-- 帖子底部信息 -->
              <div class="post-footer">
                <div class="post-tags">
                  <span
                    v-for="tag in post.tags"
                    :key="tag"
                    class="post-tag"
                    :class="'tag-' + tag"
                  >
                    {{ tag }}
                  </span>
                </div>
                <div class="post-stats">
                  <span class="stat">
                    <i class="far fa-eye"></i>
                    {{ post.views }}
                  </span>
                  <span class="stat">
                    <i class="far fa-comment"></i>
                    {{ post.commentCount }}
                  </span>
                  <span class="stat">
                    <i class="far fa-thumbs-up"></i>
                    {{ post.likes }}
                  </span>
                </div>
              </div>
            </router-link>
          </div>
        </div>

        <!-- 右侧边栏 -->
        <div class="right-sidebar">
          <!-- 通知公告框 -->
          <div class="sidebar-box">
            <div class="sidebar-header">
              <i class="fas fa-bullhorn"></i>
              <span>通知公告</span>
            </div>
            <div class="sidebar-body">
              <div
                v-for="(notice, index) in notices"
                :key="index"
                class="notice-item"
              >
                <span class="notice-tag" :class="notice.type">{{ notice.tag }}</span>
                <span class="notice-text">{{ notice.text }}</span>
                <span class="notice-date">{{ notice.date }}</span>
              </div>
            </div>
          </div>

          <!-- 热门话题框 -->
          <div class="sidebar-box">
            <div class="sidebar-header">
              <i class="fas fa-fire"></i>
              <span>热门话题</span>
            </div>
            <div class="sidebar-body">
              <div
                v-for="(topic, index) in hotTopics"
                :key="index"
                class="topic-item"
              >
                <span class="topic-rank" :class="'rank-' + (index + 1)">{{ index + 1 }}</span>
                <span class="topic-text">{{ topic.text }}</span>
                <span class="topic-heat">{{ topic.heat }}</span>
              </div>
            </div>
          </div>
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
import { listPosts } from '@/api/forum'

const activeTab = ref('hot')
const posts = ref([])
const loading = ref(false)

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`
}

function truncate(text, max = 150) {
  if (!text) return ''
  if (text.length <= max) return text
  return text.substring(0, max) + '...'
}

const filteredPosts = computed(() => {
  if (activeTab.value === 'hot') {
    return [...posts.value].sort((a, b) => (b.views || 0) - (a.views || 0))
  }
  return posts.value
})

const switchTab = (tab) => {
  activeTab.value = tab
}

const notices = ref([
  { tag: '公告', type: 'tag-notice', text: '"文化赋能乡村振兴"线上研讨会即将召开，欢迎报名参加', date: '11-17' },
  { tag: '活动', type: 'tag-activity', text: '2025年冬季边疆实践优秀案例评选开始', date: '11-15' },
  { tag: '公告', type: 'tag-notice', text: '"鸿雁"平台优秀实践库已更新，欢迎查阅参考', date: '11-10' },
  { tag: '活动', type: 'tag-activity', text: '跨学科交流区新增"适应性数字技能培训"专题', date: '11-05' }
])

const hotTopics = ref([
  { text: '边疆农产品线上营销策略', heat: '2.3w 讨论' },
  { text: '低成本物联网监测方案', heat: '1.8w 讨论' },
  { text: '非遗工艺品品牌化探索', heat: '1.5w 讨论' },
  { text: '少数民族地区数字技能培训', heat: '1.2w 讨论' },
  { text: '跨境电商实践经验分享', heat: '9.8k 讨论' }
])

onMounted(async () => {
  loading.value = true
  try {
    const result = await listPosts({ page: 1, page_size: 20 })
    posts.value = (result.items || []).map(p => ({
      id: p.id,
      author: p.author_name || '匿名用户',
      date: formatDate(p.created_at),
      team: p.team || '未指定团队',
      location: p.location || '未知',
      title: p.title,
      summary: truncate(p.content),
      tags: p.category ? [p.category] : [],
      views: p.views || 0,
      likes: p.likes || 0,
      commentCount: (p.comments || []).length
    }))
  } catch (e) {
    console.error('加载帖子失败:', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.forum-page {
  flex: 1;
  background-color: var(--color-bg-alt);
  padding: 20px 30px 40px;
}

/* 论坛标题区 */
.forum-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: var(--max-width);
  margin: 0 auto 20px;
}

.forum-title {
  font-size: 26px;
  font-weight: bold;
  color: var(--color-link);
}

.forum-subtitle {
  font-size: 14px;
  color: var(--color-text-muted);
  margin-top: 4px;
}

.new-post-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 20px;
  background-color: var(--color-link);
  color: #fff;
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-weight: 500;
  transition: background-color 0.3s;
}

.new-post-btn:hover {
  background-color: #155294;
}

/* 论坛主体布局 */
.forum-container {
  display: flex;
  gap: 30px;
  max-width: var(--max-width);
  margin: 0 auto;
}

/* 左侧帖子列表 */
.left-content {
  flex: 6;
  background-color: var(--color-bg-card);
  border: 2px solid var(--color-border);
  border-radius: var(--radius-sm);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.08);
  padding: 22px;
}

/* 排序标签 */
.content-tabs {
  display: flex;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid var(--color-border);
}

.content-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 20px;
  font-size: 16px;
  font-weight: bold;
  color: #666;
  cursor: pointer;
  margin-right: 15px;
  border-radius: var(--radius-sm) var(--radius-sm) 0 0;
  transition: all 0.3s ease;
  border: 1px solid transparent;
  border-bottom: none;
}

.content-tab:hover {
  background-color: var(--color-primary-light);
  color: var(--color-link);
}

.content-tab.active {
  color: var(--color-link);
  background-color: var(--color-primary-light);
  border-color: var(--color-border);
  border-bottom-color: var(--color-bg-card);
  position: relative;
  top: 2px;
}

/* 帖子卡片 */
.post-list {
  display: flex;
  flex-direction: column;
}

.post-card {
  display: block;
  padding: 20px 0;
  border-bottom: 2px solid var(--color-border);
  transition: all 0.3s ease;
  cursor: pointer;
}

.post-card:last-child {
  border-bottom: none;
}

.post-card:hover .post-title {
  color: #155294;
}

/* 作者信息 */
.author-info {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  gap: 15px;
}

.author-avatar {
  width: 50px;
  height: 50px;
  background-color: #e0e6ef;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #888;
  font-size: 24px;
  flex-shrink: 0;
  border: 1px solid rgba(30,58,110,.18);
}

.author-details {
  flex: 1;
}

.author-name {
  font-size: 16px;
  font-weight: bold;
  color: var(--color-text);
  margin-bottom: 4px;
}

.author-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 18px;
  color: var(--color-text-light);
  font-size: 13px;
}

.meta-item {
  display: flex;
  align-items: center;
}

.meta-item i {
  margin-right: 6px;
  color: var(--color-link);
  font-size: 13px;
}

/* 帖子标题 */
.post-title {
  font-size: 19px;
  font-weight: bold;
  color: var(--color-link);
  margin-bottom: 10px;
  transition: color 0.3s;
  line-height: 1.4;
}

/* 帖子摘要 */
.post-summary {
  font-size: 14px;
  line-height: 1.7;
  color: var(--color-text-light);
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 帖子底部 */
.post-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
}

.post-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.post-tag {
  padding: 3px 10px;
  border-radius: var(--radius-pill);
  font-size: 12px;
  font-weight: 500;
}

.tag-热门 {
  background-color: #fff0f0;
  color: var(--color-primary);
  border: 1px solid #ffcfcf;
}

.tag-最新 {
  background-color: var(--color-primary-light);
  color: var(--color-link);
  border: 1px solid rgba(30,58,110,.18);
}

.tag-求助 {
  background-color: #fff4e6;
  color: var(--el-color-warning);
  border: 1px solid #f5d9b5;
}

.tag-数字营销,
.tag-物联网,
.tag-非遗 {
  background-color: var(--color-accent-light);
  color: var(--color-accent);
  border: 1px solid rgba(30,58,110,.18);
}

.post-stats {
  display: flex;
  gap: 18px;
}

.stat {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 13px;
  color: var(--color-text-muted);
}

.stat i {
  font-size: 14px;
}

/* 右侧边栏 */
.right-sidebar {
  flex: 4;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.sidebar-box {
  background-color: var(--color-bg-card);
  border: 2px solid var(--color-border);
  border-radius: var(--radius-sm);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.sidebar-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 20px;
  background-color: var(--color-primary-light);
  border-bottom: 2px solid var(--color-border);
  font-size: 16px;
  font-weight: bold;
  color: var(--color-link);
}

.sidebar-header i {
  font-size: 16px;
}

.sidebar-body {
  padding: 12px 20px;
}

/* 通知公告 */
.notice-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 10px 0;
  border-bottom: 1px dashed var(--color-border);
}

.notice-item:last-child {
  border-bottom: none;
}

.notice-tag {
  flex-shrink: 0;
  padding: 1px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: bold;
}

.tag-notice {
  background-color: #fff0f0;
  color: var(--color-primary);
}

.tag-activity {
  background-color: var(--color-primary-light);
  color: var(--color-link);
}

.notice-text {
  flex: 1;
  font-size: 13px;
  color: var(--color-text-light);
  line-height: 1.5;
}

.notice-date {
  flex-shrink: 0;
  font-size: 12px;
  color: var(--color-text-muted);
}

/* 热门话题 */
.topic-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 0;
  border-bottom: 1px dashed var(--color-border);
}

.topic-item:last-child {
  border-bottom: none;
}

.topic-rank {
  flex-shrink: 0;
  width: 22px;
  height: 22px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  color: #fff;
  background-color: #b0b8c4;
}

.rank-1 {
  background-color: var(--color-primary);
}

.rank-2 {
  background-color: var(--el-color-warning);
}

.rank-3 {
  background-color: #f0ad4e;
}

.topic-text {
  flex: 1;
  font-size: 14px;
  color: var(--color-text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.topic-heat {
  flex-shrink: 0;
  font-size: 12px;
  color: var(--color-text-muted);
}

/* 响应式设计 */
@media (max-width: 1100px) {
  .forum-container {
    flex-direction: column;
  }

  .left-content,
  .right-sidebar {
    flex: none;
    width: 100%;
  }
}

@media (max-width: 768px) {
  .forum-page {
    padding: 15px 15px 30px;
  }

  .forum-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .forum-title {
    font-size: 22px;
  }

  .author-meta {
    flex-direction: column;
    gap: 6px;
  }

  .post-footer {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
