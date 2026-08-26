import request from './request'

export function listPosts(params = {}) {
  return request.get('/forum/posts', { params })
}

export function getPost(postId) {
  return request.get(`/forum/posts/${postId}`)
}

export function createPost(data) {
  return request.post('/forum/posts', data)
}

export function createComment(postId, data) {
  return request.post(`/forum/posts/${postId}/comments`, data)
}
