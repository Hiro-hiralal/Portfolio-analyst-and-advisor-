import { useEffect } from 'react'
import {
  Container,
  Box,
  Paper,
  Typography,
  Button,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  CircularProgress,
  Alert,
} from '@mui/material'
import { Refresh } from '@mui/icons-material'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts'
import usePortfolioStore from '../store/portfolioStore'

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8']

function Portfolio() {
  const { recommendation, loading, error, getRecommendation } = usePortfolioStore()

  useEffect(() => {
    if (!recommendation) {
      getRecommendation()
    }
  }, [])

  const handleRefresh = () => {
    getRecommendation()
  }

  if (loading) {
    return (
      <Container maxWidth="lg">
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <CircularProgress />
        </Box>
      </Container>
    )
  }

  if (error) {
    return (
      <Container maxWidth="lg">
        <Alert severity="error" sx={{ mt: 4 }}>
          {error}
        </Alert>
        <Box sx={{ mt: 2, textAlign: 'center' }}>
          <Button variant="contained" onClick={handleRefresh}>
            Try Again
          </Button>
        </Box>
      </Container>
    )
  }

  if (!recommendation) {
    return (
      <Container maxWidth="lg">
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="h6" gutterBottom>
            No portfolio recommendation yet
          </Typography>
          <Typography variant="body2" color="textSecondary" sx={{ mb: 3 }}>
            Complete your risk assessment to get a personalized portfolio recommendation
          </Typography>
          <Button variant="contained" onClick={handleRefresh}>
            Generate Recommendation
          </Button>
        </Paper>
      </Container>
    )
  }

  const allocationData = Object.entries(recommendation.recommended_allocation || {}).map(
    ([key, value]) => ({
      name: key.charAt(0).toUpperCase() + key.slice(1),
      value: value,
    })
  )

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h4" gutterBottom>
            Portfolio Recommendation
          </Typography>
          <Chip
            label={recommendation.risk_category?.toUpperCase()}
            color={
              recommendation.risk_category === 'aggressive'
                ? 'error'
                : recommendation.risk_category === 'conservative'
                ? 'success'
                : 'primary'
            }
          />
        </Box>
        <Button
          variant="outlined"
          startIcon={<Refresh />}
          onClick={handleRefresh}
        >
          Refresh
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* Performance Metrics */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Expected Performance
            </Typography>
            <Box sx={{ mt: 2 }}>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="textSecondary">
                  Expected Return
                </Typography>
                <Typography variant="h5" color="success.main">
                  {(recommendation.expected_return * 100).toFixed(2)}%
                </Typography>
              </Box>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="textSecondary">
                  Expected Volatility
                </Typography>
                <Typography variant="h5">
                  {(recommendation.expected_volatility * 100).toFixed(2)}%
                </Typography>
              </Box>
              <Box>
                <Typography variant="body2" color="textSecondary">
                  Sharpe Ratio
                </Typography>
                <Typography variant="h5">
                  {recommendation.sharpe_ratio}
                </Typography>
              </Box>
            </Box>
          </Paper>
        </Grid>

        {/* Asset Allocation */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Asset Allocation
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={allocationData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {allocationData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Holdings Table */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recommended Holdings
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Symbol</TableCell>
                    <TableCell>Name</TableCell>
                    <TableCell>Asset Class</TableCell>
                    <TableCell align="right">Allocation</TableCell>
                    <TableCell align="right">Amount</TableCell>
                    <TableCell align="right">Shares</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {recommendation.recommended_holdings?.map((holding, index) => (
                    <TableRow key={index}>
                      <TableCell>
                        <Typography variant="body2" fontWeight="bold">
                          {holding.symbol}
                        </Typography>
                      </TableCell>
                      <TableCell>{holding.name}</TableCell>
                      <TableCell>
                        <Chip
                          label={holding.asset_class}
                          size="small"
                          variant="outlined"
                        />
                      </TableCell>
                      <TableCell align="right">
                        {(holding.allocation_pct * 100).toFixed(2)}%
                      </TableCell>
                      <TableCell align="right">
                        ${holding.amount?.toFixed(2)}
                      </TableCell>
                      <TableCell align="right">
                        {holding.shares?.toFixed(2) || '-'}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>

        {/* Rationale */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recommendation Rationale
            </Typography>
            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" paragraph>
                <strong>Strategy:</strong> {recommendation.strategy}
              </Typography>
              <Typography variant="body2" paragraph>
                {recommendation.rationale?.allocation_explanation}
              </Typography>
              <Typography variant="body2" paragraph>
                <strong>Diversification:</strong> {recommendation.rationale?.diversification}
              </Typography>
              <Typography variant="body2">
                <strong>Rebalancing:</strong> {recommendation.rationale?.rebalancing}
              </Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  )
}

export default Portfolio
