import request from './request'

export function registerPersonal(data) {
  return request.post('/auth/register/personal', data)
}

export function registerEnterprise(data) {
  return request.post('/auth/register/enterprise', data)
}

export function login(data) {
  return request.post('/auth/login', data)
}

export function adminLogin() {
  return request.post('/auth/admin-login')
}

export function studentLogin() {
  return request.post('/auth/student-login')
}

export function enterpriseLogin() {
  return request.post('/auth/enterprise-login')
}

export function getMe() {
  return request.get('/auth/me')
}
