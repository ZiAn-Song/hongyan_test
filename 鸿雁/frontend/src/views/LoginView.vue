<template>
  <div class="page">
    <AppHeader />
    <div class="login-container">
      <div class="form-card">
        <div class="card-header">
          <h1><i class="fas fa-sign-in-alt"></i> 用户登录</h1>
          <p class="subtitle">请选择用户类型并输入账号信息</p>
        </div>

        <div class="form-body">
          <el-tabs v-model="activeTab" class="login-tabs">
            <el-tab-pane label="个人用户" name="personal">
              <i slot="label" class="fas fa-user"></i> 个人用户
            </el-tab-pane>
            <el-tab-pane label="政企用户" name="enterprise">
              <i slot="label" class="fas fa-building"></i> 政企用户
            </el-tab-pane>
          </el-tabs>

          <el-form
            ref="formRef"
            :model="form"
            :rules="rules"
            label-position="top"
            size="large"
            @submit.prevent="handleLogin"
          >
            <el-form-item :label="activeTab === 'personal' ? '学号' : '邮箱'" prop="account">
              <el-input
                v-model="form.account"
                :placeholder="activeTab === 'personal' ? '请输入学号' : '请输入注册邮箱'"
              >
                <template #suffix>
                  <i :class="activeTab === 'personal' ? 'fas fa-id-card' : 'fas fa-envelope'" style="color: #94a3b8"></i>
                </template>
              </el-input>
            </el-form-item>

            <el-form-item label="密码" prop="password">
              <el-input
                v-model="form.password"
                type="password"
                placeholder="请输入密码"
                show-password
                @keyup.enter="handleLogin"
              >
                <template #suffix><i class="fas fa-lock" style="color: #94a3b8"></i></template>
              </el-input>
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                class="submit-btn"
                :loading="submitting"
                @click="handleLogin"
              >
                <i class="fas fa-sign-in-alt"></i> 登录
              </el-button>
            </el-form-item>
          </el-form>

          <div class="register-link">
            还没有账号？
            <router-link :to="activeTab === 'personal' ? '/register/personal' : '/register/enterprise'">
              立即注册
            </router-link>
          </div>

          <div class="quick-login-section">
            <p class="quick-login-title">快速登录入口</p>
            <div class="quick-login-buttons">
              <button class="quick-btn student-btn" :disabled="quickLoading === 'student'" @click="handleQuickLogin('student')">
                <i class="fas fa-user-graduate"></i>
                {{ quickLoading === 'student' ? '登录中...' : '学生登入' }}
              </button>
              <button class="quick-btn enterprise-btn" :disabled="quickLoading === 'enterprise'" @click="handleQuickLogin('enterprise')">
                <i class="fas fa-building"></i>
                {{ quickLoading === 'enterprise' ? '登录中...' : '政企登入' }}
              </button>
              <button class="quick-btn admin-btn" :disabled="quickLoading === 'admin'" @click="handleQuickLogin('admin')">
                <i class="fas fa-shield-alt"></i>
                {{ quickLoading === 'admin' ? '登录中...' : '管理员入口' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <AppFooter />
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const formRef = ref(null)
const submitting = ref(false)
const quickLoading = ref(null)
const activeTab = ref('personal')

const form = reactive({
  account: '',
  password: ''
})

const rules = {
  account: [{ required: true, message: '请输入账号', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

watch(activeTab, () => {
  form.account = ''
  form.password = ''
  formRef.value?.clearValidate()
})

const handleLogin = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitting.value = true
    try {
      await authStore.login(form.account, form.password, activeTab.value)
      ElMessage.success(`欢迎回来，${authStore.userName}！`)
      const redirect = route.query.redirect || '/'
      router.push(redirect)
    } catch (err) {
      const msg = err.response?.data?.detail || err.response?.data?.message || '登录失败，请检查账号和密码'
      ElMessage.error(msg)
    } finally {
      submitting.value = false
    }
  })
}

const handleQuickLogin = async (type) => {
  quickLoading.value = type
  try {
    if (type === 'admin') {
      await authStore.adminLogin()
    } else if (type === 'student') {
      await authStore.studentLogin()
    } else if (type === 'enterprise') {
      await authStore.enterpriseLogin()
    }
    ElMessage.success(`欢迎回来，${authStore.userName}！`)
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } catch (err) {
    const msg = err.response?.data?.detail || '登录失败'
    ElMessage.error(msg)
  } finally {
    quickLoading.value = null
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 40px 20px;
  min-height: calc(100vh - var(--header-height, 90px));
  background-color: #f8fafc;
}

.form-card {
  width: 100%;
  max-width: 500px;
  background-color: var(--color-bg-card);
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.card-header {
  background-color: var(--color-primary-darker);
  color: white;
  padding: 30px;
  text-align: center;
}

.card-header h1 {
  font-size: 1.8rem;
  margin-bottom: 8px;
}

.card-header h1 i {
  margin-right: 10px;
}

.subtitle {
  font-size: 1rem;
  opacity: 0.9;
  font-weight: 300;
}

.form-body {
  padding: 30px;
}

.login-tabs {
  margin-bottom: 20px;
}

.submit-btn {
  width: 100%;
  background-color: var(--color-primary-darker);
  border-color: var(--color-primary-darker);
  font-size: 18px;
  padding: 18px;
  letter-spacing: 0.5px;
}

.submit-btn:hover {
  background: linear-gradient(to right, var(--color-primary-dark), var(--color-primary-darker));
  border-color: var(--color-primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(156, 12, 19, 0.25);
}

.register-link {
  text-align: center;
  margin-top: 20px;
  color: #666;
  font-size: 0.95rem;
}

.register-link a {
  color: var(--color-primary-darker);
  text-decoration: none;
  font-weight: 600;
}

.register-link a:hover {
  text-decoration: underline;
}

.quick-login-section {
  text-align: center;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px dashed #e0e0e0;
}

.quick-login-title {
  font-size: 0.9rem;
  color: #888;
  margin-bottom: 15px;
}

.quick-login-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

.quick-btn {
  flex: 1;
  min-width: 120px;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.quick-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.quick-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.student-btn {
  background: linear-gradient(135deg, var(--el-color-success), #2f6b4f);
}

.student-btn:hover:not(:disabled) {
  box-shadow: 0 5px 15px rgba(76, 175, 80, 0.35);
}

.enterprise-btn {
  background: linear-gradient(135deg, #1976d2, #0d47a1);
}

.enterprise-btn:hover:not(:disabled) {
  box-shadow: 0 5px 15px rgba(25, 118, 210, 0.35);
}

.admin-btn {
  background: linear-gradient(135deg, var(--ink), var(--ink));
}

.admin-btn:hover:not(:disabled) {
  box-shadow: 0 5px 15px rgba(44, 62, 80, 0.3);
}

@media (max-width: 640px) {
  .card-header {
    padding: 25px 20px;
  }

  .card-header h1 {
    font-size: 1.5rem;
  }

  .form-body {
    padding: 25px;
  }

  .login-container {
    padding: 15px;
  }
}
</style>
