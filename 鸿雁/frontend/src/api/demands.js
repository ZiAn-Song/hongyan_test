import request from './request'

export function listDemands(params = {}) {
  return request.get('/demands/', { params })
}

export function getDemand(demandId) {
  return request.get(`/demands/${demandId}`)
}

export function createDemand(data) {
  return request.post('/demands/', data)
}
