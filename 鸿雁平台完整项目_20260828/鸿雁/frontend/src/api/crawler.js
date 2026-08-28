import request from './request'

export function listArticles(params) {
  return request.get('/crawler/articles', { params })
}

export function listTodayArticles(params) {
  return request.get('/crawler/articles/today', { params })
}

export function getArticle(id) {
  return request.get(`/crawler/articles/${id}`)
}

export function getSources() {
  return request.get('/crawler/sources')
}

export function triggerCrawl(source) {
  return request.post('/crawler/trigger', null, { params: { source }, timeout: 300000 })
}

export function deleteArticle(id) {
  return request.delete(`/crawler/articles/${id}`)
}

export function clearAllArticles(source) {
  return request.delete('/crawler/articles', { params: { source } })
}
