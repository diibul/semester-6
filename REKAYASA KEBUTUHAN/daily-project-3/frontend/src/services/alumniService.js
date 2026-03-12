import api from './api'

export const fetchAlumni = async ({ page = 1, search = '' }) => {
  const { data } = await api.get('/alumni', { params: { page, search } })
  return data
}

export const createAlumni = async (payload) => {
  const { data } = await api.post('/alumni', payload)
  return data
}

export const getAlumni = async (id) => {
  const { data } = await api.get(`/alumni/${id}`)
  return data
}

export const updateAlumni = async (id, payload) => {
  const { data } = await api.put(`/alumni/${id}`, payload)
  return data
}

export const deleteAlumni = async (id) => {
  const { data } = await api.delete(`/alumni/${id}`)
  return data
}

export const trackAlumni = async (id) => {
  const { data } = await api.post(`/tracking/${id}`)
  return data
}
