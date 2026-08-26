<template>
  <div class="header-container">
    <header>
      <div class="header-left">
        <div class="logo">
          <img src="/img/logo.jpg" alt="鸿雁平台logo" />
        </div>
        <div class="site-title">
          <h1>鸿雁 | 产学研融合助力边疆发展领航者</h1>
          <p>连接地方需求，赋能边疆发展</p>
        </div>
      </div>

      <div class="nav-right">
        <nav>
          <ul>
            <li v-for="item in navItems" :key="item.path">
              <router-link :to="item.path">{{ item.label }}</router-link>
            </li>
            <li v-if="!authStore.isLoggedIn" class="auth-item">
              <router-link to="/login">登录</router-link>
            </li>
            <li v-if="authStore.isLoggedIn" class="user-item">
              <span class="user-name"><i class="fas fa-user-circle"></i> {{ authStore.userName }}</span>
              <span class="role-badge" :class="roleBadgeClass">{{ roleLabel }}</span>
              <button class="logout-btn" @click="handleLogout">退出</button>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const navItems = computed(() => {
  if (authStore.isLoggedIn && authStore.isAdmin) {
    return [
      { path: '/', label: '网站首页' },
      { path: '/comprehensive', label: '综合' },
      { path: '/crawler', label: '边疆资讯' },
      { path: '/forum', label: '论坛' },
      { path: '/demand', label: '需求' },
      { path: '/achievement', label: '成果展示' },
      { path: '/team', label: '团队信息' }
    ]
  }
  if (authStore.isLoggedIn && authStore.isEnterprise) {
    return [
      { path: '/', label: '网站首页' },
      { path: '/comprehensive', label: '综合' },
      { path: '/publish', label: '发布需求' },
      { path: '/crawler', label: '边疆资讯' },
      { path: '/forum', label: '论坛' },
      { path: '/demand', label: '需求' },
      { path: '/achievement', label: '成果展示' },
      { path: '/team', label: '团队信息' }
    ]
  }
  if (authStore.isLoggedIn && authStore.isPersonal) {
    return [
      { path: '/', label: '网站首页' },
      { path: '/comprehensive', label: '综合' },
      { path: '/crawler', label: '边疆资讯' },
      { path: '/forum', label: '论坛' },
      { path: '/demand', label: '需求' },
      { path: '/achievement', label: '成果展示' },
      { path: '/team', label: '团队信息' }
    ]
  }
  return [
    { path: '/', label: '网站首页' },
    { path: '/comprehensive', label: '综合' },
    { path: '/crawler', label: '边疆资讯' },
    { path: '/forum', label: '论坛' },
    { path: '/demand', label: '需求' },
    { path: '/achievement', label: '成果展示' },
    { path: '/team', label: '团队信息' },
    { path: '/register/enterprise', label: '政企登入' },
    { path: '/register/personal', label: '个人登入' }
  ]
})

const roleLabel = computed(() => {
  if (authStore.isAdmin) return '管理员'
  if (authStore.isEnterprise) return '政企'
  if (authStore.isPersonal) return '学生'
  return ''
})

const roleBadgeClass = computed(() => {
  if (authStore.isAdmin) return 'badge-admin'
  if (authStore.isEnterprise) return 'badge-enterprise'
  return 'badge-student'
})

const handleLogout = () => {
  authStore.logout()
  ElMessage.success('已退出登录')
  router.push('/')
}
</script>

<style scoped>
.header-container {
  position: relative;
  width: 100%;
}

header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 5%;
  background-color: var(--color-primary-light);
  box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
  position: relative;
  z-index: 10;
}

.header-left {
  display: flex;
  align-items: center;
}

.logo {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  overflow: hidden;
  margin-right: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.logo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 12px;
}

.site-title h1 {
  font-size: 24px;
  color: white;
  font-weight: 700;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

.site-title p {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
  margin-top: 3px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.nav-right {
  display: flex;
  align-items: center;
  width: 60%;
}

nav {
  width: 100%;
}

nav ul {
  display: flex;
  width: 100%;
  justify-content: space-between;
  gap: 5px;
  align-items: center;
}

nav li {
  padding: 16px 22px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  border-radius: 8px;
  font-size: 18px;
  text-align: center;
  flex: 1;
  min-width: 0;
  white-space: nowrap;
  background-color: rgba(255, 255, 255, 0.15);
}

nav li a {
  color: inherit;
  text-decoration: none;
  display: block;
  width: 100%;
  height: 100%;
}

nav li:hover {
  background-color: rgba(255, 255, 255, 0.3);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(255, 255, 255, 0.2);
}

nav li.router-link-active {
  background-color: white;
  color: var(--color-primary);
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.4);
}

nav li::after {
  content: '';
  position: absolute;
  bottom: 8px;
  left: 50%;
  width: 0;
  height: 3px;
  background-color: white;
  transition: all 0.3s;
  transform: translateX(-50%);
}

nav li:hover::after {
  width: 70%;
}

nav li.router-link-active::after {
  width: 70%;
  background-color: var(--color-primary);
}

.auth-item {
  background-color: rgba(255, 255, 255, 0.25) !important;
  border: 2px solid rgba(255, 255, 255, 0.4);
}

.user-item {
  display: flex;
  align-items: center;
  gap: 10px;
  background-color: transparent !important;
  padding: 8px 12px !important;
  flex: 0 0 auto !important;
}

.user-name {
  color: white;
  font-size: 16px;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 6px;
}

.logout-btn {
  padding: 6px 16px;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 6px;
  color: white;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s;
  white-space: nowrap;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.35);
}

.role-badge {
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.badge-admin {
  background: linear-gradient(135deg, #6a1b9a, #8e24aa);
  color: white;
}

.badge-enterprise {
  background: linear-gradient(135deg, #e65100, #f57c00);
  color: white;
}

.badge-student {
  background: linear-gradient(135deg, #1565c0, #1976d2);
  color: white;
}

@media (max-width: 1024px) {
  header {
    flex-direction: column;
    padding: 15px 20px;
  }

  .header-left {
    width: 100%;
    justify-content: space-between;
    margin-bottom: 15px;
  }

  .nav-right {
    width: 100%;
    justify-content: center;
  }

  nav ul {
    width: 100%;
    justify-content: space-between;
    flex-wrap: wrap;
  }

  nav li {
    padding: 12px 15px;
    font-size: 15px;
    flex: 0 0 auto;
  }
}

@media (max-width: 480px) {
  .header-left {
    flex-direction: column;
    text-align: center;
  }

  .logo {
    margin-right: 0;
    margin-bottom: 10px;
  }

  nav ul {
    gap: 3px;
    flex-wrap: wrap;
    justify-content: center;
  }

  nav li {
    padding: 8px 10px;
    font-size: 13px;
    flex: 0 0 auto;
  }

  .user-item {
    flex-direction: column;
    gap: 6px;
  }
}
</style>
