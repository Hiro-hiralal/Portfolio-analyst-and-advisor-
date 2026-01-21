import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Authentication
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
  logout: () => api.post('/auth/logout'),
}

// User profile
export const userAPI = {
  getProfile: () => api.get('/user/profile'),
  updateProfile: (data) => api.put('/user/profile', data),
  getPreferences: () => api.get('/user/preferences'),
  updatePreferences: (data) => api.put('/user/preferences', data),
}

// Risk assessment
export const riskAPI = {
  getQuestionnaire: () => api.get('/risk/questionnaire'),
  submitQuestionnaire: (responses) => api.post('/risk/questionnaire', responses),
  getProfile: () => api.get('/risk/profile'),
}

// Portfolio
export const portfolioAPI = {
  getRecommendation: () => api.post('/portfolio/recommendation', {}),
  getRecommendations: () => api.get('/portfolio/recommendations'),
  getCurrent: () => api.get('/portfolio/current'),
  runScenario: (data) => api.post('/portfolio/scenario', data),
  getScenarios: () => api.get('/portfolio/scenarios'),
  runMonteCarlo: (data) => api.post('/portfolio/monte-carlo', data),
}

// Market data
export const marketAPI = {
  getOverview: () => api.get('/market/overview'),
  getSecurityInfo: (symbol) => api.get(`/market/security/${symbol}`),
  getPrice: (symbol) => api.get(`/market/price/${symbol}`),
}

export default api
