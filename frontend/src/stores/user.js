import { defineStore } from 'pinia'
import api from '../api'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    refresh: localStorage.getItem('refresh') || '',
    user: JSON.parse(localStorage.getItem('user') || 'null'),
  }),
  actions: {
    async login(username, password) {
      const res = await api.post('/token/', { username, password })
      this.token = res.access
      this.refresh = res.refresh
      localStorage.setItem('token', res.access)
      localStorage.setItem('refresh', res.refresh)
      await this.fetchUser()
    },
    async fetchUser() {
      const user = await api.get('/accounts/me/')
      this.user = user
      localStorage.setItem('user', JSON.stringify(user))
    },
    logout() {
      this.token = ''
      this.refresh = ''
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('refresh')
      localStorage.removeItem('user')
    },
  },
})
