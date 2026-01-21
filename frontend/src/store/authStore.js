import { create } from 'zustand'
import { authAPI } from '../services/api'

const useAuthStore = create((set) => ({
  user: null,
  token: localStorage.getItem('token'),
  isAuthenticated: !!localStorage.getItem('token'),
  loading: false,
  error: null,

  login: async (email, password) => {
    set({ loading: true, error: null })
    try {
      const response = await authAPI.login({ email, password })
      const { access_token } = response.data
      localStorage.setItem('token', access_token)

      // Get user data
      const userResponse = await authAPI.getMe()
      set({
        token: access_token,
        user: userResponse.data,
        isAuthenticated: true,
        loading: false,
      })
      return true
    } catch (error) {
      set({
        error: error.response?.data?.detail || 'Login failed',
        loading: false,
      })
      return false
    }
  },

  register: async (email, password, full_name) => {
    set({ loading: true, error: null })
    try {
      await authAPI.register({ email, password, full_name })
      // After registration, log in
      return await useAuthStore.getState().login(email, password)
    } catch (error) {
      set({
        error: error.response?.data?.detail || 'Registration failed',
        loading: false,
      })
      return false
    }
  },

  logout: () => {
    localStorage.removeItem('token')
    set({
      user: null,
      token: null,
      isAuthenticated: false,
    })
  },

  fetchUser: async () => {
    set({ loading: true })
    try {
      const response = await authAPI.getMe()
      set({ user: response.data, loading: false })
    } catch (error) {
      set({ loading: false })
      if (error.response?.status === 401) {
        useAuthStore.getState().logout()
      }
    }
  },

  clearError: () => set({ error: null }),
}))

export default useAuthStore
