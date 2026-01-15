import { create } from 'zustand'
import { portfolioAPI } from '../services/api'

const usePortfolioStore = create((set) => ({
  recommendation: null,
  scenarios: [],
  monteCarloResult: null,
  loading: false,
  error: null,

  getRecommendation: async () => {
    set({ loading: true, error: null })
    try {
      const response = await portfolioAPI.getRecommendation()
      set({ recommendation: response.data, loading: false })
      return response.data
    } catch (error) {
      set({
        error: error.response?.data?.detail || 'Failed to get recommendation',
        loading: false,
      })
      return null
    }
  },

  runScenario: async (scenarioData) => {
    set({ loading: true, error: null })
    try {
      const response = await portfolioAPI.runScenario(scenarioData)
      set((state) => ({
        scenarios: [...state.scenarios, response.data],
        loading: false,
      }))
      return response.data
    } catch (error) {
      set({
        error: error.response?.data?.detail || 'Failed to run scenario',
        loading: false,
      })
      return null
    }
  },

  runMonteCarlo: async (params) => {
    set({ loading: true, error: null })
    try {
      const response = await portfolioAPI.runMonteCarlo(params)
      set({ monteCarloResult: response.data, loading: false })
      return response.data
    } catch (error) {
      set({
        error: error.response?.data?.detail || 'Failed to run Monte Carlo simulation',
        loading: false,
      })
      return null
    }
  },

  clearScenarios: () => set({ scenarios: [] }),
  clearError: () => set({ error: null }),
}))

export default usePortfolioStore
