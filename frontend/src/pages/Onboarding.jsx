import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Container,
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Stepper,
  Step,
  StepLabel,
  Alert,
  CircularProgress,
} from '@mui/material'
import { userAPI } from '../services/api'
import useAuthStore from '../store/authStore'

const steps = ['Personal Information', 'Financial Goals', 'Complete']

function Onboarding() {
  const navigate = useNavigate()
  const { fetchUser } = useAuthStore()
  const [activeStep, setActiveStep] = useState(0)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [formData, setFormData] = useState({
    age: '',
    investable_amount: '',
    monthly_contribution: '',
    time_horizon: '',
    location: '',
  })

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
    setError(null)
  }

  const handleNext = () => {
    setActiveStep((prevStep) => prevStep + 1)
  }

  const handleBack = () => {
    setActiveStep((prevStep) => prevStep - 1)
  }

  const handleSubmit = async () => {
    setLoading(true)
    setError(null)

    try {
      await userAPI.updateProfile({
        age: parseInt(formData.age),
        investable_amount: parseFloat(formData.investable_amount),
        monthly_contribution: parseFloat(formData.monthly_contribution),
        time_horizon: parseInt(formData.time_horizon),
        location: formData.location,
      })

      await fetchUser()
      setActiveStep(2)

      setTimeout(() => {
        navigate('/risk-assessment')
      }, 2000)
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to update profile')
    } finally {
      setLoading(false)
    }
  }

  const renderStepContent = (step) => {
    switch (step) {
      case 0:
        return (
          <Box>
            <TextField
              fullWidth
              margin="normal"
              label="Age"
              name="age"
              type="number"
              value={formData.age}
              onChange={handleChange}
              required
              inputProps={{ min: 18, max: 100 }}
            />
            <TextField
              fullWidth
              margin="normal"
              label="Investable Amount ($)"
              name="investable_amount"
              type="number"
              value={formData.investable_amount}
              onChange={handleChange}
              required
              inputProps={{ min: 0, step: 1000 }}
              helperText="Total amount you plan to invest"
            />
            <TextField
              fullWidth
              margin="normal"
              label="Location"
              name="location"
              value={formData.location}
              onChange={handleChange}
              placeholder="e.g., New York, USA"
            />
          </Box>
        )
      case 1:
        return (
          <Box>
            <TextField
              fullWidth
              margin="normal"
              label="Monthly Contribution ($)"
              name="monthly_contribution"
              type="number"
              value={formData.monthly_contribution}
              onChange={handleChange}
              inputProps={{ min: 0, step: 100 }}
              helperText="Amount you plan to invest monthly"
            />
            <TextField
              fullWidth
              margin="normal"
              label="Investment Time Horizon (years)"
              name="time_horizon"
              type="number"
              value={formData.time_horizon}
              onChange={handleChange}
              required
              inputProps={{ min: 1, max: 50 }}
              helperText="How long until you need this money?"
            />
          </Box>
        )
      case 2:
        return (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            <Typography variant="h5" gutterBottom color="success.main">
              Profile Setup Complete!
            </Typography>
            <Typography variant="body1" color="textSecondary">
              Redirecting to risk assessment...
            </Typography>
          </Box>
        )
      default:
        return null
    }
  }

  const isStepValid = () => {
    switch (activeStep) {
      case 0:
        return formData.age && formData.investable_amount
      case 1:
        return formData.time_horizon
      default:
        return true
    }
  }

  return (
    <Container maxWidth="md">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Welcome! Let's set up your profile
        </Typography>
        <Typography variant="body1" color="textSecondary">
          This information helps us provide personalized portfolio recommendations
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Paper sx={{ p: 4 }}>
        <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>

        {renderStepContent(activeStep)}

        {activeStep < 2 && (
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
            <Button onClick={handleBack} disabled={activeStep === 0}>
              Back
            </Button>
            <Button
              variant="contained"
              onClick={activeStep === 1 ? handleSubmit : handleNext}
              disabled={!isStepValid() || loading}
            >
              {loading ? (
                <CircularProgress size={24} />
              ) : activeStep === 1 ? (
                'Complete'
              ) : (
                'Next'
              )}
            </Button>
          </Box>
        )}
      </Paper>
    </Container>
  )
}

export default Onboarding
