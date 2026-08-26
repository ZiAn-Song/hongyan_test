import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  login as apiLogin,
  adminLogin as apiAdminLogin,
  studentLogin as apiStudentLogin,
  enterpriseLogin as apiEnterpriseLogin,
  getMe,
  registerPersonal,
  registerEnterprise
} from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('access_token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user_info') || 'null'))

  const isLoggedIn = computed(() => !!token.value)
  const userName = computed(() => user.value?.name || '')
  const userType = computed(() => user.value?.user_type || '')
  const userRole = computed(() => user.value?.role || '')
  const isPersonal = computed(() => userType.value === 'personal')
  const isEnterprise = computed(() => userType.value === 'enterprise')
  const isAdmin = computed(() => userRole.value === 'admin')

  function setAuth(tokenValue, userValue) {
    token.value = tokenValue
    user.value = userValue
    localStorage.setItem('access_token', tokenValue)
    localStorage.setItem('user_info', JSON.stringify(userValue))
  }

  async function login(account, password, user_type) {
    const data = await apiLogin({ account, password, user_type })
    setAuth(data.access_token, {
      id: data.user_id,
      name: data.name,
      user_type: data.user_type,
      role: data.role
    })
    return data
  }

  async function adminLogin() {
    const data = await apiAdminLogin()
    setAuth(data.access_token, {
      id: data.user_id,
      name: data.name,
      user_type: data.user_type,
      role: data.role
    })
    return data
  }

  async function studentLogin() {
    const data = await apiStudentLogin()
    setAuth(data.access_token, {
      id: data.user_id,
      name: data.name,
      user_type: data.user_type,
      role: data.role
    })
    return data
  }

  async function enterpriseLogin() {
    const data = await apiEnterpriseLogin()
    setAuth(data.access_token, {
      id: data.user_id,
      name: data.name,
      user_type: data.user_type,
      role: data.role
    })
    return data
  }

  async function registerPersonalUser(formData) {
    return await registerPersonal(formData)
  }

  async function registerEnterpriseUser(formData) {
    return await registerEnterprise(formData)
  }

  async function fetchMe() {
    try {
      const data = await getMe()
      user.value = { ...user.value, ...data }
      localStorage.setItem('user_info', JSON.stringify(user.value))
      return data
    } catch {
      logout()
    }
  }

  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_info')
  }

  return {
    token,
    user,
    isLoggedIn,
    userName,
    userType,
    userRole,
    isPersonal,
    isEnterprise,
    isAdmin,
    setAuth,
    login,
    adminLogin,
    studentLogin,
    enterpriseLogin,
    registerPersonalUser,
    registerEnterpriseUser,
    fetchMe,
    logout
  }
})
