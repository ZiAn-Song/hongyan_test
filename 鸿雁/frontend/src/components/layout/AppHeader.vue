<template>
  <div class="header-container">
    <!-- 报头 masthead：双细线文书风 -->
    <header>
      <div class="masthead-top">
        <div class="header-left">
          <div class="logo">
            <img src="/img/logo.jpg" alt="鸿雁平台logo" />
          </div>
          <div class="site-title">
            <h1>鸿雁<span class="title-divider">·</span>东西部协作智能资源对接平台</h1>
            <p>连接地方需求 · 赋能边疆发展</p>
          </div>
        </div>

        <div class="nav-right">
          <nav>
            <ul>
              <li v-for="item in navItems" :key="item.path">
                <router-link :to="item.path" :class="{ active: route.path === item.path }">{{ item.label }}</router-link>
              </li>
              <li v-if="!authStore.isLoggedIn" class="auth-item">
                <router-link to="/login" class="login-link">登录</router-link>
              </li>
              <li v-if="authStore.isLoggedIn" class="user-item">
                <span class="user-name">{{ authStore.userName }}</span>
                <span class="role-badge" :class="roleBadgeClass">{{ roleLabel }}</span>
                <button class="logout-btn" @click="handleLogout">退出</button>
              </li>
            </ul>
          </nav>
        </div>
      </div>
      <div class="masthead-rule"></div>
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
  background: var(--paper);
}

header {
  padding: 0 4%;
  position: relative;
  z-index: 10;
}

.masthead-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 0 14px;
  max-width: var(--max-width);
  margin: 0 auto;
  flex-wrap: wrap;
  gap: 10px;
}

.header-left {
  display: flex;
  align-items: center;
}

.logo {
  width: 52px;
  height: 52px;
  border-radius: 3px;
  overflow: hidden;
  margin-right: 14px;
  border: 1px solid var(--rule);
  flex-shrink: 0;
}
.logo img { width: 100%; height: 100%; object-fit: cover; }

.site-title h1 {
  font-family: var(--font-serif);
  font-size: 21px;
  font-weight: 700;
  letter-spacing: 2px;
  color: var(--ink);
  line-height: 1.4;
}
.title-divider { color: var(--color-accent); margin: 0 6px; font-weight: 400; }
.site-title p {
  font-size: 11px;
  letter-spacing: 3.5px;
  color: var(--ink-3);
  margin-top: 2px;
}

.nav-right nav ul {
  display: flex;
  align-items: center;
  gap: 2px;
  flex-wrap: wrap;
}
nav a {
  display: block;
  padding: 7px 13px;
  font-size: 13.5px;
  color: var(--ink-2);
  letter-spacing: 1px;
  border-bottom: 2px solid transparent;
  transition: color 0.2s, border-color 0.2s;
}
nav a:hover { color: var(--color-primary); }
nav a.active {
  color: var(--color-primary);
  font-weight: 650;
  border-bottom-color: var(--color-primary);
}

.auth-item .login-link {
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
  border-radius: var(--radius-sm);
  padding: 6px 18px;
  margin-left: 8px;
  font-weight: 600;
}
.auth-item .login-link:hover { background: var(--color-primary); color: #fff; }

.user-item { display: flex; align-items: center; gap: 8px; }
.user-name { font-size: 13px; color: var(--ink); font-weight: 600; }

.role-badge {
  font-size: 10.5px;
  padding: 1px 8px;
  border: 1px solid;
  border-radius: 2px;
  letter-spacing: 1.5px;
}
.badge-admin { color: var(--color-accent); border-color: rgba(163, 58, 42, 0.4); background: var(--color-accent-light); }
.badge-enterprise { color: var(--color-primary); border-color: rgba(30, 58, 110, 0.35); background: var(--color-primary-light); }
.badge-student { color: var(--ink-2); border-color: var(--rule); background: var(--paper-2); }

.logout-btn {
  border: none;
  background: none;
  font-size: 12.5px;
  color: var(--ink-3);
  cursor: pointer;
  letter-spacing: 1px;
  padding: 4px 2px;
}
.logout-btn:hover { color: var(--color-accent); }

/* 报头双细线：粗 + 细，文书气质 */
.masthead-rule {
  border-top: 3px double var(--ink);
  position: relative;
}
.masthead-rule::after {
  content: "";
  position: absolute;
  left: 0; right: 0; top: 3px;
  border-top: 1px solid var(--rule);
}

@media (max-width: 960px) {
  .masthead-top { flex-direction: column; align-items: flex-start; }
}
</style>
