import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
  headers: {
    Accept: 'application/json',     // 👈 obligatorio para DRF
  },
  
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

export default api
