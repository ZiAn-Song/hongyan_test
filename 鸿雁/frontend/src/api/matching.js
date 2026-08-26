import request from './request'

export function matchSuppliesForDemand(demandId, params = {}) {
  return request.get(`/matching/demands/${demandId}/supplies`, { params })
}

export function matchDemandsForSupply(supplyId, params = {}) {
  return request.get(`/matching/supplies/${supplyId}/demands`, { params })
}
