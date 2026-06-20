import api from './api'

export const login = async (payload) => {
  const { data } = await api.post('/login', payload)
  return data
}

export const logout = async () => {
  const { data } = await api.post('/logout')
  return data
}

export const getMe = async () => {
  const { data } = await api.get('/me')
  return data
}
