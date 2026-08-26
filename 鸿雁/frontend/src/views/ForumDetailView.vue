<template>
  <div class="page">
    <AppHeader />

    <div class="topic-page">
      <div class="topic-container">
        <!-- 主内容区域 -->
        <div class="main-content" v-if="post">
          <!-- 返回链接 -->
          <router-link to="/forum" class="back-link">
            <i class="fas fa-arrow-left"></i>
            返回论坛
          </router-link>

          <!-- 作者信息区域 -->
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

          <!-- 帖子大标题 -->
          <h1 class="topic-main-title">{{ post.title }}</h1>

          <!-- 正文内容 -->
          <div class="topic-content">
            <div class="content-block" v-for="(block, index) in contentBlocks" :key="index">
              {{ block }}
            </div>
          </div>

          <!-- 标签与统计区域 -->
          <div class="tags-stats-container">
            <!-- 标签区域 -->
            <div class="tags-section">
              <div class="tags-title">话题标签</div>
              <div class="tags-list">
                <span class="tag" v-for="tag in tags" :key="tag">{{ tag }}</span>
              </div>
            </div>

            <!-- 统计区域 -->
            <div class="stats-section">
              <div class="stats-title">话题统计</div>
              <div class="stats-container">
                <div class="stat-item">
                  <div class="stat-icon">
                    <i class="far fa-eye"></i>
                  </div>
                  <div class="stat-value">{{ post.views.toLocaleString() }}</div>
                  <div class="stat-label">浏览</div>
                </div>

                <div class="stat-item">
                  <div class="stat-icon">
                    <i class="far fa-thumbs-up"></i>
                  </div>
                  <div class="stat-value">{{ post.likes }}</div>
                  <div class="stat-label">点赞</div>
                </div>

                <div class="stat-item">
                  <div class="stat-icon">
                    <i class="far fa-comment"></i>
                  </div>
                  <div class="stat-value">{{ formattedComments.length }}</div>
                  <div class="stat-label">评论</div>
                </div>
              </div>
            </div>
          </div>

          <!-- 评论部分 -->
          <div class="comments-section">
            <div class="comments-title">
              评论
              <span class="comments-count">({{ formattedComments.length }})</span>
            </div>

            <!-- 评论输入框 -->
            <div class="comment-input-box">
              <div class="comment-input-avatar">
                <i class="fas fa-user"></i>
              </div>
              <div class="comment-input-main">
                <textarea
                  v-model="newComment"
                  class="comment-textarea"
                  placeholder="发表你的看法..."
                  rows="3"
                ></textarea>
                <div class="comment-input-footer">
                  <span class="comment-tip">
                    <i class="fas fa-info-circle"></i>
                    请友善交流，遵守社区规范
                  </span>
                  <button
                    class="comment-submit-btn"
                    :disabled="!newComment.trim() || submittingComment"
                    @click="submitComment"
                  >
                    {{ submittingComment ? '发表中...' : '发表评论' }}
                  </button>
                </div>
              </div>
            </div>

            <!-- 评论列表 -->
            <div class="comment-list">
              <div
                v-for="(comment, index) in formattedComments"
                :key="index"
                class="comment-item"
              >
                <div class="comment-avatar">
                  <i class="fas fa-user"></i>
                </div>
                <div class="comment-details">
                  <div class="comment-author">{{ comment.author }}</div>
                  <div class="comment-meta">
                    <span><i class="far fa-clock"></i> {{ comment.date }}</span>
                  </div>
                  <div class="comment-text">{{ comment.text }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 帖子未找到 -->
        <div class="main-content not-found" v-else>
          <i class="fas fa-exclamation-circle"></i>
          <h2>未找到该帖子</h2>
          <p>帖子可能已被删除或链接有误</p>
          <router-link to="/forum" class="back-link">
            <i class="fas fa-arrow-left"></i>
            返回论坛
          </router-link>
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
import { useRoute } from 'vue-router'
import { getPost, createComment } from '@/api/forum'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const route = useRoute()
const authStore = useAuthStore()
const postId = Number(route.params.id)
const post = ref(null)
const newComment = ref('')
const submittingComment = ref(false)

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`
}

const contentBlocks = computed(() => {
  if (!post.value?.content) return []
  return post.value.content.split('\n').filter(b => b.trim())
})

const tags = computed(() => {
  if (!post.value) return []
  return post.value.category ? [post.value.category] : []
})

const formattedComments = computed(() => {
  if (!post.value?.comments) return []
  return post.value.comments.map(c => ({
    author: c.author_name || '匿名用户',
    date: formatDate(c.created_at),
    text: c.content
  }))
})

const submitComment = async () => {
  const text = newComment.value.trim()
  if (!text) return

  submittingComment.value = true
  try {
    const newCmt = await createComment(postId, { content: text })
    post.value.comments.push(newCmt)
    newComment.value = ''
    ElMessage.success('评论发表成功')
  } catch (err) {
    const msg = err.response?.data?.detail || '评论发表失败'
    ElMessage.error(msg)
  } finally {
    submittingComment.value = false
  }
}

onMounted(async () => {
  try {
    const data = await getPost(postId)
    post.value = {
      ...data,
      author: data.author_name || '匿名用户',
      date: formatDate(data.created_at),
      views: data.views || 0,
      likes: data.likes || 0
    }
  } catch (e) {
    console.error('加载帖子失败:', e)
    post.value = null
  }
})
</script>

<style scoped>
.page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.topic-page {
  flex: 1;
  background-color: var(--color-bg-alt);
  padding: 20px 30px 40px;
}

.topic-container {
  max-width: var(--max-width);
  margin: 0 auto;
}

/* 主内容区域 */
.main-content {
  background-color: var(--color-bg-card);
  border: 2px solid #d0d7e0;
  border-radius: var(--radius-sm);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.08);
  padding: 28px 30px;
}

/* 返回链接 */
.back-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: var(--color-link);
  margin-bottom: 22px;
  transition: color 0.3s;
}

.back-link:hover {
  color: #155294;
}

/* 作者信息区域 */
.author-info {
  display: flex;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 25px;
  border-bottom: 2px solid #eaeaea;
  gap: 20px;
}

.author-avatar {
  width: 80px;
  height: 80px;
  background-color: #e0e6ef;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #888;
  font-size: 38px;
  flex-shrink: 0;
  border: 1px solid #c5d9f0;
}

.author-details {
  flex: 1;
}

.author-name {
  font-size: 22px;
  font-weight: bold;
  color: var(--color-text);
  margin-bottom: 10px;
}

.author-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 25px;
  color: var(--color-text-light);
  font-size: 14px;
}

.meta-item {
  display: flex;
  align-items: center;
}

.meta-item i {
  margin-right: 6px;
  color: var(--color-link);
  font-size: 14px;
}

/* 帖子大标题 */
.topic-main-title {
  font-size: 26px;
  font-weight: bold;
  color: var(--color-link);
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #eaeaea;
  line-height: 1.4;
}

/* 正文内容 */
.topic-content {
  font-size: 16px;
  line-height: 1.8;
  margin-bottom: 28px;
}

.content-block {
  margin-bottom: 16px;
  padding: 14px 16px;
  border-radius: var(--radius-sm);
  background-color: #fafbfc;
  border-left: 4px solid #c5d9f0;
  color: var(--color-text);
}

.content-block:last-child {
  margin-bottom: 0;
}

/* 图片区域 */
.topic-images {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-top: 25px;
  padding-top: 20px;
  border-top: 1px solid #eaeaea;
}

.topic-image {
  flex: 1;
  min-width: 200px;
  height: 130px;
  background-color: #f0f7ff;
  border-radius: var(--radius-sm);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--color-link);
  font-size: 13px;
  border: 2px dashed #c5d9f0;
}

.topic-image i {
  font-size: 32px;
  margin-bottom: 8px;
}

/* 标签与统计区域 */
.tags-stats-container {
  margin-top: 28px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: var(--radius-md);
}

.tags-section {
  margin-bottom: 22px;
}

.tags-title,
.stats-title {
  font-size: 18px;
  font-weight: bold;
  color: var(--color-link);
  margin-bottom: 14px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eaeaea;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.tag {
  padding: 7px 16px;
  background-color: #e8f2ff;
  color: var(--color-link);
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-weight: 500;
  border: 1px solid #c5d9f0;
}

/* 统计区域 */
.stats-container {
  display: flex;
  justify-content: space-between;
  gap: 15px;
}

.stat-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 18px 15px;
  background-color: var(--color-bg-card);
  border-radius: var(--radius-sm);
  border: 1px solid #e0e6ef;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.stat-icon {
  font-size: 24px;
  color: var(--color-link);
  margin-bottom: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: var(--color-link);
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: var(--color-text-light);
}

/* 评论部分 */
.comments-section {
  margin-top: 35px;
  padding-top: 25px;
  border-top: 2px solid #eaeaea;
}

.comments-title {
  font-size: 20px;
  font-weight: bold;
  color: var(--color-link);
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eaeaea;
}

.comments-count {
  font-size: 16px;
  font-weight: normal;
  color: var(--color-text-muted);
}

/* 评论输入框 */
.comment-input-box {
  display: flex;
  gap: 15px;
  margin-bottom: 25px;
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: var(--radius-sm);
  border: 1px solid #e0e6ef;
}

.comment-input-avatar {
  width: 44px;
  height: 44px;
  background-color: #e0e6ef;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #888;
  font-size: 18px;
  flex-shrink: 0;
}

.comment-input-main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.comment-textarea {
  width: 100%;
  border: 1px solid #d0d7e0;
  border-radius: var(--radius-sm);
  padding: 10px 12px;
  font-size: 14px;
  font-family: var(--font-family);
  resize: vertical;
  outline: none;
  transition: border-color 0.3s;
}

.comment-textarea:focus {
  border-color: var(--color-link);
}

.comment-input-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 10px;
}

.comment-tip {
  font-size: 12px;
  color: var(--color-text-muted);
}

.comment-tip i {
  margin-right: 4px;
}

.comment-submit-btn {
  padding: 7px 22px;
  background-color: var(--color-link);
  color: #fff;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.comment-submit-btn:hover:not(:disabled) {
  background-color: #155294;
}

.comment-submit-btn:disabled {
  background-color: #b0b8c4;
  cursor: not-allowed;
}

/* 评论列表 */
.comment-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.comment-item {
  display: flex;
  align-items: flex-start;
  padding: 16px;
  background-color: var(--color-bg-card);
  border-radius: var(--radius-sm);
  border-left: 4px solid #d0d7e0;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.comment-avatar {
  width: 44px;
  height: 44px;
  background-color: #e0e6ef;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #888;
  font-size: 16px;
  flex-shrink: 0;
  margin-right: 15px;
}

.comment-details {
  flex: 1;
}

.comment-author {
  font-weight: bold;
  color: var(--color-text);
  margin-bottom: 6px;
  font-size: 15px;
}

.comment-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  color: var(--color-text-light);
  font-size: 13px;
  margin-bottom: 10px;
}

.comment-meta span {
  display: flex;
  align-items: center;
}

.comment-meta i {
  margin-right: 5px;
  color: var(--color-link);
  font-size: 12px;
}

.comment-text {
  font-size: 15px;
  line-height: 1.6;
  color: var(--color-text-light);
}

/* 未找到帖子 */
.not-found {
  text-align: center;
  padding: 60px 30px;
}

.not-found i {
  font-size: 56px;
  color: var(--color-text-muted);
  margin-bottom: 20px;
}

.not-found h2 {
  font-size: 22px;
  color: var(--color-text);
  margin-bottom: 10px;
}

.not-found p {
  color: var(--color-text-muted);
  margin-bottom: 20px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .topic-page {
    padding: 15px 15px 30px;
  }

  .main-content {
    padding: 20px;
  }

  .author-info {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }

  .author-meta {
    flex-direction: column;
    gap: 8px;
    align-items: center;
  }

  .topic-images {
    flex-direction: column;
  }

  .topic-image {
    min-width: 100%;
  }

  .stats-container {
    flex-direction: column;
  }

  .comment-item {
    flex-direction: column;
  }

  .comment-avatar {
    margin-right: 0;
    margin-bottom: 12px;
  }

  .comment-input-box {
    flex-direction: column;
  }

  .comment-input-avatar {
    margin-bottom: 10px;
  }
}
</style>
