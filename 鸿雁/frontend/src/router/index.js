import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
    meta: { title: '鸿雁 - 线上社会实践云平台' }
  },
  {
    path: '/publish',
    name: 'publish',
    component: () => import('@/views/PublishView.vue'),
    meta: { title: '发布需求 - 鸿雁', requiresAuth: true, enterpriseOnly: true }
  },
  {
    path: '/forum',
    name: 'forum',
    component: () => import('@/views/ForumView.vue'),
    meta: { title: '万里边疆 - 实时论坛' }
  },
  {
    path: '/forum/:id',
    name: 'forum-detail',
    component: () => import('@/views/ForumDetailView.vue'),
    meta: { title: '帖子详情 - 论坛' }
  },
  {
    path: '/team',
    name: 'team',
    component: () => import('@/views/TeamView.vue'),
    meta: { title: '团队信息 - 鸿雁' }
  },
  {
    path: '/demand',
    name: 'demand',
    component: () => import('@/views/DemandView.vue'),
    meta: { title: '需求大厅 - 鸿雁' }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue'),
    meta: { title: '登录 - 鸿雁' }
  },
  {
    path: '/register/personal',
    name: 'register-personal',
    component: () => import('@/views/PersonalRegisterView.vue'),
    meta: { title: '个人注册 - 鸿雁' }
  },
  {
    path: '/register/enterprise',
    name: 'register-enterprise',
    component: () => import('@/views/EnterpriseRegisterView.vue'),
    meta: { title: '政企注册 - 鸿雁' }
  },
  {
    path: '/category/:type',
    name: 'category',
    component: () => import('@/views/CategoryView.vue'),
    meta: { title: '需求分类 - 鸿雁' }
  },
  {
    path: '/achievement',
    name: 'achievement',
    component: () => import('@/views/AchievementView.vue'),
    meta: { title: '成果展示 - 鸿雁' }
  },
  {
    path: '/crawler',
    name: 'crawler',
    component: () => import('@/views/CrawlerView.vue'),
    meta: { title: '边疆资讯 - 鸿雁' }
  },
  {
    path: '/comprehensive',
    name: 'comprehensive',
    component: () => import('@/views/ComprehensiveView.vue'),
    meta: { title: '综合平台 - 鸿雁' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.meta.enterpriseOnly && !authStore.isEnterprise) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

router.afterEach((to) => {
  if (to.meta.title) {
    document.title = to.meta.title
  }
})

export default router
