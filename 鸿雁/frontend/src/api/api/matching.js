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

// ===== 双向自由对接（真实使用逻辑）=====
// 需求方：自由描述需求 → 三级漏斗匹配资源库
export function freestyleMatch(text, params = {}) {
  return request.post('/matching/v2/freestyle', { text, ...params })
}
// 供给方：输入能力画像 → 反向匹配边疆需求库
export function reverseMatch(text, params = {}) {
  return request.post('/matching/v2/reverse', { text, ...params })
}
