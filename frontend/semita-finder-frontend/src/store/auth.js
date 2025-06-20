// stores/auth.js
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    usuario: null,
  }),
  actions: {
    setToken(token) {
      this.token = token
      localStorage.setItem('token', token)
    },
    logout() {
      this.token = null
      this.usuario = null
      localStorage.removeItem('token')
    }
  }
})
