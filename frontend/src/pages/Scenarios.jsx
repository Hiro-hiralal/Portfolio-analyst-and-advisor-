import { useState, useEffect } from 'react'
import {
  Container,
  Box,
  Paper,
  Typography,
  Button,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Tabs,
  Tab,
  Alert,
  CircularProgress,
} from '@mui/material'
import { PlayArrow, Refresh } from '@mui/icons-material'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import usePortfolioStore from '../store/portfolioStore'
import { portfolioAPI } from '../services/api'

function TabPanel({ children, value, index }) {
  return (
    <div hidden={value !== index}>
      {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
    </div>
  )
}

function Scenarios() {
  const { scenarios, monteCarloResult, runScenario, runMonteCarlo, clearScenarios, loading } =
    usePortfolioStore()

  const [tabValue, setTabValue] = useState(0)
  const [availableScenarios, setAvailableScenarios] = useState([])
  const [selectedScenario, setSelectedScenario] = useState('')
  const [customScenario, setCustomScenario] = useState({
    stock_return: 0,
    bond_return: 0,
  })
  const [monteCarloParams, setMonteCarloParams] = useState({
    num_simulations: 1000,
    time_horizon: 10,
  })

  useEffect(() => {
    fetchAvailableScenarios()
  }, [])

  const fetchAvailableScenarios = async () => {
    try {
      const response = await portfolioAPI.getScenarios()
      setAvailableScenarios(response.data.scenarios)
      if (response.data.scenarios.length > 0) {
        setSelectedScenario(response.data.scenarios[0].id)
      }
    } catch (error) {
      console.error('Error fetching scenarios:', error)
    }
  }

  const handleRunPredefinedScenario = async () => {
    await runScenario({
      scenario_type: 'predefined',
      scenario_name: selectedScenario,
    })
  }

  const handleRunCustomScenario = async () => {
    await runScenario({
      scenario_type: 'custom',
      stock_return: parseFloat(customScenario.stock_return) / 100,
      bond_return: parseFloat(customScenario.bond_return) / 100,
    })
  }

  const handleRunMonteCarlo = async () => {
    await runMonteCarlo(monteCarloParams)
  }

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue)
  }

  const percentileData = monteCarloResult
    ? Object.entries(monteCarloResult.percentiles).map(([key, value]) => ({
        percentile: key,
        value: value,
      }))
    : []

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h4" gutterBottom>
            Scenario Analysis
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Test your portfolio under different market conditions
          </Typography>
        </Box>
        <Button
          variant="outlined"
          startIcon={<Refresh />}
          onClick={clearScenarios}
        >
          Clear Results
        </Button>
      </Box>

      <Paper sx={{ mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange}>
          <Tab label="Predefined Scenarios" />
          <Tab label="Custom Scenario" />
          <Tab label="Monte Carlo Simulation" />
        </Tabs>

        {/* Predefined Scenarios Tab */}
        <TabPanel value={tabValue} index={0}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Select Scenario</InputLabel>
                <Select
                  value={selectedScenario}
                  label="Select Scenario"
                  onChange={(e) => setSelectedScenario(e.target.value)}
                >
                  {availableScenarios.map((scenario) => (
                    <MenuItem key={scenario.id} value={scenario.id}>
                      {scenario.name} - {scenario.description}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <Button
                variant="contained"
                size="large"
                fullWidth
                startIcon={<PlayArrow />}
                onClick={handleRunPredefinedScenario}
                disabled={loading || !selectedScenario}
                sx={{ height: '56px' }}
              >
                {loading ? <CircularProgress size={24} /> : 'Run Scenario'}
              </Button>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Custom Scenario Tab */}
        <TabPanel value={tabValue} index={1}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Stock Market Return (%)"
                type="number"
                value={customScenario.stock_return}
                onChange={(e) =>
                  setCustomScenario({ ...customScenario, stock_return: e.target.value })
                }
                inputProps={{ step: 0.1 }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Bond Market Return (%)"
                type="number"
                value={customScenario.bond_return}
                onChange={(e) =>
                  setCustomScenario({ ...customScenario, bond_return: e.target.value })
                }
                inputProps={{ step: 0.1 }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <Button
                variant="contained"
                size="large"
                fullWidth
                startIcon={<PlayArrow />}
                onClick={handleRunCustomScenario}
                disabled={loading}
                sx={{ height: '56px' }}
              >
                {loading ? <CircularProgress size={24} /> : 'Run Custom Scenario'}
              </Button>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Monte Carlo Tab */}
        <TabPanel value={tabValue} index={2}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Number of Simulations"
                type="number"
                value={monteCarloParams.num_simulations}
                onChange={(e) =>
                  setMonteCarloParams({
                    ...monteCarloParams,
                    num_simulations: parseInt(e.target.value),
                  })
                }
                inputProps={{ min: 100, max: 10000, step: 100 }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <TextField
                fullWidth
                label="Time Horizon (years)"
                type="number"
                value={monteCarloParams.time_horizon}
                onChange={(e) =>
                  setMonteCarloParams({
                    ...monteCarloParams,
                    time_horizon: parseInt(e.target.value),
                  })
                }
                inputProps={{ min: 1, max: 50 }}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <Button
                variant="contained"
                size="large"
                fullWidth
                startIcon={<PlayArrow />}
                onClick={handleRunMonteCarlo}
                disabled={loading}
                sx={{ height: '56px' }}
              >
                {loading ? <CircularProgress size={24} /> : 'Run Simulation'}
              </Button>
            </Grid>
          </Grid>
        </TabPanel>
      </Paper>

      {/* Scenario Results */}
      {scenarios.length > 0 && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Scenario Results
          </Typography>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Scenario</TableCell>
                  <TableCell align="right">Projected Value</TableCell>
                  <TableCell align="right">Gain/Loss</TableCell>
                  <TableCell align="right">Gain/Loss %</TableCell>
                  <TableCell align="right">Recovery Time</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {scenarios.map((scenario, index) => (
                  <TableRow key={index}>
                    <TableCell>{scenario.scenario_name}</TableCell>
                    <TableCell align="right">
                      ${scenario.projected_value.toLocaleString()}
                    </TableCell>
                    <TableCell
                      align="right"
                      sx={{
                        color: scenario.expected_gain_loss >= 0 ? 'success.main' : 'error.main',
                      }}
                    >
                      ${scenario.expected_gain_loss.toLocaleString()}
                    </TableCell>
                    <TableCell
                      align="right"
                      sx={{
                        color: scenario.expected_gain_loss_pct >= 0 ? 'success.main' : 'error.main',
                      }}
                    >
                      {scenario.expected_gain_loss_pct >= 0 ? '+' : ''}
                      {scenario.expected_gain_loss_pct.toFixed(2)}%
                    </TableCell>
                    <TableCell align="right">
                      {scenario.recovery_time_months
                        ? `${scenario.recovery_time_months} months`
                        : '-'}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      )}

      {/* Monte Carlo Results */}
      {monteCarloResult && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Monte Carlo Results
              </Typography>
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" color="textSecondary">
                  Expected Value
                </Typography>
                <Typography variant="h5" gutterBottom>
                  ${monteCarloResult.expected_value.toLocaleString()}
                </Typography>

                <Typography variant="body2" color="textSecondary" sx={{ mt: 2 }}>
                  Best Case (90th percentile)
                </Typography>
                <Typography variant="h6" color="success.main" gutterBottom>
                  ${monteCarloResult.best_case.toLocaleString()}
                </Typography>

                <Typography variant="body2" color="textSecondary" sx={{ mt: 2 }}>
                  Worst Case (10th percentile)
                </Typography>
                <Typography variant="h6" color="error.main" gutterBottom>
                  ${monteCarloResult.worst_case.toLocaleString()}
                </Typography>

                <Typography variant="body2" color="textSecondary" sx={{ mt: 2 }}>
                  Probability of Positive Return
                </Typography>
                <Typography variant="h6">
                  {(monteCarloResult.probability_of_positive_return * 100).toFixed(1)}%
                </Typography>
              </Box>
            </Paper>
          </Grid>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Outcome Distribution
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={percentileData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="percentile" />
                  <YAxis />
                  <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
                  <Legend />
                  <Bar dataKey="value" fill="#8884d8" name="Portfolio Value" />
                </BarChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>
        </Grid>
      )}
    </Container>
  )
}

export default Scenarios
