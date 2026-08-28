<template>
  <div class="left-content">
    <article
      v-for="item in activities"
      :key="item.id"
      class="activity-item"
    >
      <div class="activity-content-left">
        <div class="activity-header">
          <h4>{{ item.title }}</h4>
          <div class="activity-meta">
            <span>发布人：{{ item.author }}</span>
            <span>{{ item.date }}</span>
          </div>
        </div>
        <div class="activity-content">
          <div class="activity-location">
            <i class="fas fa-map-pin"></i>
            实践所在地：{{ item.location }}
          </div>
          <p class="activity-text">{{ item.text }}</p>
        </div>
      </div>
      <div class="activity-image">
        <img :src="item.image" alt="团队实践活动图片" />
      </div>
    </article>

    <div class="left-more-teams">
      <router-link to="/team">点击了解更多团队</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { listTeams } from '@/api/teams'

const fallbackActivities = [
  {
    id: 0,
    title: '智农先锋',
    author: '队长·张明',
    date: '2025-09-01',
    location: '山东·泰安',
    text: '完成第一轮用户访谈并整理问卷结果，下一步准备数据采集。团队已与XX县农业局完成对接，正在梳理电商直播需求清单。',
    image: '/img/pic2.jpg'
  },
  {
    id: 1,
    title: '文旅筑梦',
    author: '队长·李华',
    date: '2025-08-20',
    location: '山东·青岛',
    text: '取得地方文化馆合作，开始历史素材数字化采集。目前正在整理非遗文化资料，计划下月完成数据库框架搭建。',
    image: '/img/pic2.jpg'
  },
  {
    id: 2,
    title: '医护连心',
    author: '队长·王芳',
    date: '2025-08-15',
    location: '山东·临沂',
    text: '基层卫生站远程诊疗系统需求调研已完成，正在撰写调研报告。团队计划与信息中心合作开发原型系统。',
    image: '/img/pic2.jpg'
  }
]

const activities = ref(fallbackActivities)

onMounted(async () => {
  try {
    const result = await listTeams({ page: 1, page_size: 3 })
    if (result.items && result.items.length > 0) {
      activities.value = result.items.map(t => ({
        id: t.id,
        title: t.team_name || '未命名团队',
        author: t.leader_name || '未知',
        date: t.created_at ? new Date(t.created_at).toLocaleDateString('zh-CN') : '',
        location: t.university || '未知高校',
        text: t.team_description ? t.team_description.substring(0, 150) + '...' : '暂无描述',
        image: '/img/pic2.jpg'
      }))
    }
  } catch (e) {
    console.error('加载活动数据失败，使用默认数据:', e)
  }
})
</script>

<style scoped>
.left-content {
  flex: 1.2;
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding-right: 10px;
  border-right: 1px solid var(--color-border);
}

.activity-item {
  border: 1px solid var(--color-border);
  border-radius: 10px;
  overflow: hidden;
  transition: all 0.3s;
  background-color: var(--color-bg-card);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  min-height: 160px;
  display: flex;
  flex-direction: row;
  width: 100%;
}

.activity-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
}

.activity-content-left {
  flex: 2.2;
  display: flex;
  flex-direction: column;
}

.activity-header {
  background-color: var(--color-accent);
  color: white;
  padding: 10px 16px;
  min-height: 48px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  flex-shrink: 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

.activity-header h4 {
  font-size: 16px;
  margin-bottom: 3px;
  font-weight: 600;
  line-height: 1.2;
}

.activity-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.8);
}

.activity-content {
  padding: 12px 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.activity-location {
  color: var(--color-accent);
  font-weight: 600;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  font-size: 13px;
  flex-shrink: 0;
}

.activity-location i {
  margin-right: 6px;
  font-size: 14px;
  color: var(--color-accent);
}

.activity-text {
  color: var(--color-text-light);
  line-height: 1.5;
  font-size: 13px;
  flex: 1;
}

.activity-image {
  flex: 1.5;
  background-color: var(--paper-2);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
  border-left: 1px solid var(--color-border);
  min-width: 140px;
  overflow: hidden;
}

.activity-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 6px;
}

.left-more-teams {
  text-align: center;
  margin-top: 15px;
  width: 100%;
}

.left-more-teams a {
  display: inline-block;
  padding: 10px 25px;
  background-color: var(--color-accent);
  color: white;
  border-radius: 25px;
  text-decoration: none;
  font-weight: 500;
  font-size: 14px;
  transition: all 0.3s;
  box-shadow: 0 2px 5px rgba(74, 144, 226, 0.2);
}

.left-more-teams a:hover {
  background-color: var(--color-accent-dark);
  transform: scale(1.02);
  box-shadow: 0 4px 8px rgba(74, 144, 226, 0.3);
}

@media (max-width: 1024px) {
  .left-content {
    flex: 1;
    margin-left: 0;
    padding-right: 0;
    border-right: none;
  }

  .activity-item {
    min-height: 140px;
  }
}

@media (max-width: 768px) {
  .activity-item {
    flex-direction: column;
  }

  .activity-image {
    border-left: none;
    border-top: 1px solid var(--color-border);
    min-height: 90px;
    min-width: 100%;
  }

  .activity-header {
    padding: 8px 14px;
    min-height: 44px;
  }

  .activity-header h4 {
    font-size: 15px;
  }

  .activity-content {
    padding: 10px 14px;
  }

  .activity-text {
    font-size: 12px;
  }
}
</style>
