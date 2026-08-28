import request from './request'

export function listTeams(params = {}) {
  return request.get('/teams/', { params })
}

export function getTeam(teamId) {
  return request.get(`/teams/${teamId}`)
}

export function createTeam(data) {
  return request.post('/teams/', data)
}
