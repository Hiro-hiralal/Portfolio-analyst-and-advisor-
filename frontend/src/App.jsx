import { Routes, Route, Navigate } from 'react-router-dom'
import { Box } from '@mui/material'
import useAuthStore from './store/authStore'
import Layout from './components/Layout'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Onboarding from './pages/Onboarding'
import RiskAssessment from './pages/RiskAssessment'
import Portfolio from './pages/Portfolio'
import Scenarios from './pages/Scenarios'

function ProtectedRoute({ children }) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)
  return isAuthenticated ? children : <Navigate to="/login" />
}

function App() {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Dashboard />} />
          <Route path="onboarding" element={<Onboarding />} />
          <Route path="risk-assessment" element={<RiskAssessment />} />
          <Route path="portfolio" element={<Portfolio />} />
          <Route path="scenarios" element={<Scenarios />} />
        </Route>
      </Routes>
    </Box>
  )
}

export default App
