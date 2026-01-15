# Financial Portfolio Analyzer & Advisor

An intelligent, data-driven application that provides personalized investment portfolio recommendations based on real-time financial market data, user risk profiles, and financial goals. Built with FastAPI backend and React frontend.

## Features

### Core Functionality
- **User Authentication**: Secure JWT-based authentication system
- **Risk Assessment**: Interactive questionnaire to determine user risk tolerance (Conservative to Aggressive)
- **Portfolio Recommendations**: AI-powered portfolio allocation using Modern Portfolio Theory (MPT)
- **Real-time Market Data**: Integration with Yahoo Finance for current market prices and indices
- **Interactive Dashboards**: Visual analytics with charts and graphs
- **Scenario Analysis**: Test portfolio performance under various market conditions
- **Monte Carlo Simulations**: Probabilistic modeling of portfolio outcomes

### Investment Features
- Diversified asset allocation across stocks, bonds, alternatives, and cash
- Specific ETF recommendations for each asset class
- Expected returns, volatility, and Sharpe ratio calculations
- Predefined scenarios (market crash, recession, high inflation, etc.)
- Custom scenario builder
- Multi-year portfolio projections with confidence intervals

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.9+)
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: JWT tokens with bcrypt password hashing
- **Financial Data**: yfinance (Yahoo Finance API)
- **Portfolio Optimization**: PyPortfolioOpt, NumPy, SciPy
- **API Documentation**: Automatic OpenAPI (Swagger) docs

### Frontend
- **Framework**: React 18 with Vite
- **UI Library**: Material-UI (MUI)
- **State Management**: Zustand
- **Routing**: React Router v6
- **Charts**: Recharts
- **HTTP Client**: Axios

## Project Structure

```
Portfolio-analyst-and-advisor-/
├── backend/
│   ├── app/
│   │   ├── core/           # Configuration, database, security
│   │   ├── models/         # SQLAlchemy models and Pydantic schemas
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic (portfolio, market data)
│   │   └── main.py         # FastAPI application entry point
│   ├── requirements.txt    # Python dependencies
│   └── .env.example       # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── components/     # Reusable React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API client
│   │   ├── store/          # Zustand state management
│   │   ├── App.jsx         # Main application component
│   │   └── main.jsx        # React entry point
│   ├── package.json        # Node.js dependencies
│   └── vite.config.js      # Vite configuration
├── PRD.md                  # Product Requirements Document
└── README.md               # This file
```

## Getting Started

### Prerequisites
- Python 3.9 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

5. Update the `.env` file with your settings:
```env
DATABASE_URL=sqlite:///./portfolio.db
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

6. Run the backend server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Usage Guide

### 1. Registration & Onboarding
1. Create an account with email and password
2. Complete the onboarding form with:
   - Age
   - Investable amount
   - Monthly contribution
   - Investment time horizon
   - Location

### 2. Risk Assessment
1. Navigate to "Risk Assessment"
2. Answer 8 questions about:
   - Investment time horizon
   - Reaction to losses
   - Primary investment goals
   - Loss tolerance
   - Investment experience
   - Emergency savings
   - Income stability
   - Market knowledge
3. Receive a risk score (0-100) and category (Conservative to Aggressive)

### 3. Portfolio Recommendation
1. Navigate to "Portfolio"
2. Click "Generate Recommendation"
3. View your personalized portfolio:
   - Asset allocation breakdown
   - Specific ETF holdings
   - Expected returns and volatility
   - Sharpe ratio
   - Investment rationale

### 4. Scenario Analysis
1. Navigate to "Scenarios"
2. Choose from:
   - **Predefined Scenarios**: Market crash, recession, high inflation, etc.
   - **Custom Scenarios**: Set your own market return assumptions
   - **Monte Carlo Simulation**: Run probabilistic projections
3. Analyze results and recommendations

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info

### User Profile
- `GET /user/profile` - Get user profile
- `PUT /user/profile` - Update profile
- `GET /user/preferences` - Get investment preferences
- `PUT /user/preferences` - Update preferences

### Risk Assessment
- `GET /risk/questionnaire` - Get questionnaire questions
- `POST /risk/questionnaire` - Submit responses
- `GET /risk/profile` - Get risk profile

### Portfolio
- `POST /portfolio/recommendation` - Generate recommendation
- `GET /portfolio/recommendations` - Get recommendation history
- `POST /portfolio/scenario` - Run scenario analysis
- `GET /portfolio/scenarios` - Get available scenarios
- `POST /portfolio/monte-carlo` - Run Monte Carlo simulation

### Market Data
- `GET /market/overview` - Get market indices overview
- `GET /market/security/{symbol}` - Get security information
- `GET /market/price/{symbol}` - Get current price

## Risk Profiles

The application calculates risk scores based on questionnaire responses and categorizes users:

- **Conservative (0-24)**: 60% Bonds, 30% Stocks, 5% Alternatives, 5% Cash
- **Moderate Conservative (25-44)**: 45% Bonds, 45% Stocks, 7% Alternatives, 3% Cash
- **Moderate (45-64)**: 30% Bonds, 60% Stocks, 8% Alternatives, 2% Cash
- **Moderate Aggressive (65-79)**: 15% Bonds, 75% Stocks, 9% Alternatives, 1% Cash
- **Aggressive (80-100)**: 5% Bonds, 85% Stocks, 10% Alternatives, 0% Cash

## ETF Recommendations

The system recommends low-cost, diversified ETFs:

- **US Large Cap**: VTI (Vanguard Total Stock Market)
- **US Mid Cap**: VO (Vanguard Mid-Cap)
- **US Small Cap**: VB (Vanguard Small-Cap)
- **International**: VXUS (Vanguard Total International Stock)
- **Bonds**: BND (Vanguard Total Bond Market)
- **Corporate Bonds**: VCIT (Vanguard Intermediate-Term Corporate Bond)
- **REITs**: VNQ (Vanguard Real Estate)
- **Gold**: GLD (SPDR Gold Trust)

## Security Considerations

- Passwords are hashed using bcrypt
- JWT tokens for stateless authentication
- CORS configured for frontend-backend communication
- SQL injection protection via SQLAlchemy ORM
- Input validation with Pydantic models

## Development

### Running Tests
```bash
# Backend tests (when implemented)
cd backend
pytest

# Frontend tests (when implemented)
cd frontend
npm test
```

### Building for Production

Backend:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Frontend:
```bash
cd frontend
npm run build
npm run preview
```

## Deployment

### Backend (Railway/Heroku/AWS)
1. Set environment variables in platform
2. Update `DATABASE_URL` to PostgreSQL
3. Deploy backend application
4. Run database migrations

### Frontend (Vercel/Netlify)
1. Set `VITE_API_URL` environment variable
2. Connect repository
3. Deploy with automatic builds

## Limitations & Disclaimers

**Important**: This application is for educational and informational purposes only. It is NOT:
- Professional financial advice
- A substitute for a licensed financial advisor
- Guaranteed to be accurate or profitable
- Suitable for making actual investment decisions

Market data may be delayed. Past performance does not guarantee future results. Always consult with a qualified financial professional before making investment decisions.

## Future Enhancements

- Tax-loss harvesting recommendations
- Integration with brokerage accounts (Plaid)
- Mobile app (React Native)
- Advanced portfolio optimization algorithms
- News sentiment analysis
- Automated rebalancing alerts
- Multi-currency support
- Social features (community insights)

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is for educational purposes. See LICENSE file for details.

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

## Acknowledgments

- Financial data provided by Yahoo Finance
- Portfolio optimization theory based on Modern Portfolio Theory (Markowitz)
- UI components from Material-UI
- Chart library: Recharts

---

**Version**: 1.0.0
**Last Updated**: January 2026
