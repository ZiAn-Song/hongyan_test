import request from './request'

export function matchSuppliesForDemand(demandId, params = {}) {
  return request.get(`/matching/demands/${demandId}/supplies`, { params })
}

export function matchDemandsForSupply(supplyId, params = {}) {
  return request.get(`/matching/supplies/${supplyId}/demands`, { params })
}

// ===== v2 三级漏斗智能匹配（DeepSeek 研判 + 向量召回 + 三因子可信度 + 历史范式）=====
export function matchDemandV2(demandId, params = {}) {
  return request.get(`/matching/v2/demands/${demandId}/match`, { params })
}
