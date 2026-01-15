import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Container,
  Box,
  Paper,
  Typography,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormControl,
  FormLabel,
  Button,
  Alert,
  CircularProgress,
  Stepper,
  Step,
  StepLabel,
} from '@mui/material'
import { riskAPI } from '../services/api'

function RiskAssessment() {
  const navigate = useNavigate()
  const [questions, setQuestions] = useState([])
  const [responses, setResponses] = useState({})
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)
  const [activeStep, setActiveStep] = useState(0)

  useEffect(() => {
    fetchQuestionnaire()
  }, [])

  const fetchQuestionnaire = async () => {
    try {
      const response = await riskAPI.getQuestionnaire()
      setQuestions(response.data.questions)
      // Initialize responses
      const initialResponses = {}
      response.data.questions.forEach((q) => {
        initialResponses[q.id] = ''
      })
      setResponses(initialResponses)
    } catch (error) {
      setError('Failed to load questionnaire')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (questionId, value) => {
    setResponses({
      ...responses,
      [questionId]: value,
    })
  }

  const handleNext = () => {
    setActiveStep((prevStep) => prevStep + 1)
  }

  const handleBack = () => {
    setActiveStep((prevStep) => prevStep - 1)
  }

  const handleSubmit = async () => {
    setSubmitting(true)
    setError(null)

    try {
      const response = await riskAPI.submitQuestionnaire(responses)
      setSuccess(true)
      setTimeout(() => {
        navigate('/portfolio')
      }, 2000)
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to submit questionnaire')
    } finally {
      setSubmitting(false)
    }
  }

  const isStepComplete = () => {
    if (activeStep >= questions.length) return true
    const currentQuestion = questions[activeStep]
    return responses[currentQuestion.id] !== ''
  }

  if (loading) {
    return (
      <Container maxWidth="md">
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <CircularProgress />
        </Box>
      </Container>
    )
  }

  return (
    <Container maxWidth="md">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Risk Assessment
        </Typography>
        <Typography variant="body1" color="textSecondary">
          Answer these questions to determine your investment risk profile
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 3 }}>
          Risk assessment completed! Redirecting to portfolio...
        </Alert>
      )}

      <Paper sx={{ p: 4 }}>
        <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
          {questions.map((question, index) => (
            <Step key={question.id}>
              <StepLabel>Q{index + 1}</StepLabel>
            </Step>
          ))}
        </Stepper>

        {activeStep < questions.length && (
          <Box>
            <FormControl component="fieldset" fullWidth>
              <FormLabel component="legend" sx={{ mb: 3 }}>
                <Typography variant="h6">
                  {activeStep + 1}. {questions[activeStep].text}
                </Typography>
              </FormLabel>
              <RadioGroup
                value={responses[questions[activeStep].id]}
                onChange={(e) => handleChange(questions[activeStep].id, e.target.value)}
              >
                {questions[activeStep].options.map((option) => (
                  <FormControlLabel
                    key={option.value}
                    value={option.value}
                    control={<Radio />}
                    label={option.label}
                    sx={{ mb: 1 }}
                  />
                ))}
              </RadioGroup>
            </FormControl>

            <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
              <Button
                onClick={handleBack}
                disabled={activeStep === 0}
              >
                Back
              </Button>
              <Button
                variant="contained"
                onClick={activeStep === questions.length - 1 ? handleSubmit : handleNext}
                disabled={!isStepComplete() || submitting}
              >
                {submitting ? (
                  <CircularProgress size={24} />
                ) : activeStep === questions.length - 1 ? (
                  'Submit'
                ) : (
                  'Next'
                )}
              </Button>
            </Box>
          </Box>
        )}
      </Paper>
    </Container>
  )
}

export default RiskAssessment
