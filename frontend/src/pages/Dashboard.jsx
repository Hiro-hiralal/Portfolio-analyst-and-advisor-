import { useState, useEffect } from 'react'
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  CircularProgress,
} from '@mui/material'
import {
  TrendingUp,
  AccountBalance,
  ShowChart,
  Assessment,
} from '@mui/icons-material'
import { useNavigate } from 'react-router-dom'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'
import usePortfolioStore from '../store/portfolioStore'
import { marketAPI } from '../services/api'

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8']

function StatCard({ title, value, icon, color }) {
  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Box>
            <Typography color="textSecondary" gutterBottom variant="body2">
              {title}
            </Typography>
            <Typography variant="h5" component="div">
              {value}
            </Typography>
          </Box>
          <Box
            sx={{
              backgroundColor: color,
              borderRadius: '50%',
              p: 1.5,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            {icon}
          </Box>
        </Box>
      </CardContent>
    </Card>
  )
}

function Dashboard() {
  const navigate = useNavigate()
  const { recommendation, getRecommendation, loading } = usePortfolioStore()
  const [marketData, setMarketData] = useState(null)
  const [loadingMarket, setLoadingMarket] = useState(true)

  useEffect(() => {
    fetchMarketData()
  }, [])

  const fetchMarketData = async () => {
    try {
      const response = await marketAPI.getOverview()
      setMarketData(response.data)
    } catch (error) {
      console.error('Error fetching market data:', error)
    } finally {
      setLoadingMarket(false)
    }
  }

  const handleGetRecommendation = async () => {
    await getRecommendation()
  }

  const allocationData = recommendation?.recommended_allocation
    ? Object.entries(recommendation.recommended_allocation).map(([key, value]) => ({
        name: key.charAt(0).toUpperCase() + key.slice(1),
        value: value,
      }))
    : []

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Dashboard
        </Typography>
        <Typography variant="body1" color="textSecondary">
          Welcome to your portfolio dashboard
        </Typography>
      </Box>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Portfolio Value"
            value={recommendation ? `$${recommendation.expected_return * 100000 || 0}` : '-'}
            icon={<AccountBalance sx={{ color: 'white' }} />}
            color="#1976d2"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Expected Return"
            value={recommendation ? `${(recommendation.expected_return * 100).toFixed(1)}%` : '-'}
            icon={<TrendingUp sx={{ color: 'white' }} />}
            color="#4caf50"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Risk Level"
            value={recommendation?.risk_category || 'Not Set'}
            icon={<Assessment sx={{ color: 'white' }} />}
            color="#ff9800"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Sharpe Ratio"
            value={recommendation?.sharpe_ratio || '-'}
            icon={<ShowChart sx={{ color: 'white' }} />}
            color="#9c27b0"
          />
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {/* Asset Allocation */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: 400 }}>
            <Typography variant="h6" gutterBottom>
              Asset Allocation
            </Typography>
            {loading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 300 }}>
                <CircularProgress />
              </Box>
            ) : recommendation ? (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={allocationData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, value }) => `${name}: ${value}%`}
                    outerRadius={80}
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
            ) : (
              <Box sx={{ textAlign: 'center', mt: 4 }}>
                <Typography variant="body1" color="textSecondary" gutterBottom>
                  No portfolio recommendation yet
                </Typography>
                <Button
                  variant="contained"
                  onClick={handleGetRecommendation}
                  sx={{ mt: 2 }}
                >
                  Get Recommendation
                </Button>
              </Box>
            )}
          </Paper>
        </Grid>

        {/* Market Overview */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: 400 }}>
            <Typography variant="h6" gutterBottom>
              Market Overview
            </Typography>
            {loadingMarket ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 300 }}>
                <CircularProgress />
              </Box>
            ) : marketData?.indices?.length > 0 ? (
              <Box>
                {marketData.indices.map((index) => (
                  <Box
                    key={index.symbol}
                    sx={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      py: 2,
                      borderBottom: '1px solid #e0e0e0',
                    }}
                  >
                    <Typography variant="body1">{index.name}</Typography>
                    <Box sx={{ textAlign: 'right' }}>
                      <Typography variant="body1">
                        ${index.price?.toFixed(2) || 0}
                      </Typography>
                      <Typography
                        variant="body2"
                        sx={{
                          color: index.change_pct >= 0 ? 'success.main' : 'error.main',
                        }}
                      >
                        {index.change_pct >= 0 ? '+' : ''}
                        {index.change_pct?.toFixed(2) || 0}%
                      </Typography>
                    </Box>
                  </Box>
                ))}
              </Box>
            ) : (
              <Typography variant="body2" color="textSecondary">
                No market data available
              </Typography>
            )}
          </Paper>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Quick Actions
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mt: 2 }}>
              <Button
                variant="contained"
                onClick={() => navigate('/risk-assessment')}
              >
                Take Risk Assessment
              </Button>
              <Button
                variant="contained"
                onClick={() => navigate('/portfolio')}
              >
                View Portfolio Details
              </Button>
              <Button
                variant="contained"
                onClick={() => navigate('/scenarios')}
              >
                Run Scenario Analysis
              </Button>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  )
}

export default Dashboard
