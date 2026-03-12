import api from './api'

export const fetchResults = async ({ page = 1 } = {}) => {
  const { data } = await api.get('/results', { params: { page } })
  return data
}

export const getResult = async (id) => {
  const { data } = await api.get(`/results/${id}`)
  return data
}

export const verifyResult = async (id, action) => {
  const { data } = await api.put(`/results/${id}/verify`, { action })
  return data
}
