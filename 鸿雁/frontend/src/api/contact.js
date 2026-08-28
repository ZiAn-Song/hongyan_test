import request from './request'

// ===== 站内对接通道 =====
export function startThread(payload) {
  return request.post('/contact/threads', payload)
}
export function listThreads() {
  return request.get('/contact/threads')
}
export function getThreadMessages(threadId) {
  return request.get(`/contact/threads/${threadId}/messages`)
}
export function sendThreadMessage(threadId, content) {
  return request.post(`/contact/threads/${threadId}/messages`, { content })
}
export function unreadCount() {
  return request.get('/contact/unread-count')
}
