# 📸 App Walkthrough - Visual Guide

## Complete Screen-by-Screen Guide to Portfolio Advisor

---

## 🔐 Screen 1: Login Page

**URL:** `/login`

**Layout:**
```
┌─────────────────────────────────────┐
│                                     │
│       Portfolio Advisor             │
│          (Large Title)              │
│                                     │
│           Sign In                   │
│        (Subtitle)                   │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Email Address                 │  │
│  │ [text input field]            │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Password                      │  │
│  │ [password field]              │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │      SIGN IN (Blue Button)    │  │
│  └───────────────────────────────┘  │
│                                     │
│   Don't have an account? Sign Up    │
│         (clickable link)            │
│                                     │
└─────────────────────────────────────┘
```

**Features:**
- Clean, centered design with white paper card
- Blue Material-UI theme
- Form validation
- Error messages appear in red alert box above form
- Responsive for mobile (full width on small screens)

**Mobile View:** Perfect for Pixel 10, vertical scrolling if needed

---

## 📝 Screen 2: Registration Page

**URL:** `/register`

**Layout:**
```
┌─────────────────────────────────────┐
│       Portfolio Advisor             │
│        Create Account               │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Full Name                     │  │
│  │ [text input]                  │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Email Address                 │  │
│  │ [text input]                  │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Password                      │  │
│  │ [password field]              │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Confirm Password              │  │
│  │ [password field]              │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │      SIGN UP (Button)         │  │
│  └───────────────────────────────┘  │
│                                     │
│   Already have account? Sign In     │
└─────────────────────────────────────┘
```

**Validation:**
- Password must be 6+ characters
- Passwords must match
- Shows validation errors in red

---

## 🎯 Screen 3: Onboarding (Profile Setup)

**URL:** `/onboarding`

**Layout:**
```
┌─────────────────────────────────────┐
│  Welcome! Let's set up your profile │
│                                     │
│  [Stepper: Step 1 ● ○ ○]           │
│                                     │
│  Personal Information               │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Age                           │  │
│  │ [number input]                │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Investable Amount ($)         │  │
│  │ [number input]                │  │
│  │ Total amount you plan to invest│  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Location                      │  │
│  │ [text input: e.g., New York]  │  │
│  └───────────────────────────────┘  │
│                                     │
│  [Back]              [Next →]       │
└─────────────────────────────────────┘
```

**Step 2:**
```
│  Financial Goals                    │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Monthly Contribution ($)      │  │
│  │ [number input]                │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Investment Time Horizon (yrs) │  │
│  │ [number input]                │  │
│  │ How long until you need money? │  │
│  └───────────────────────────────┘  │
│                                     │
│  [← Back]          [Complete]       │
```

**After Completion:** Redirects to Risk Assessment

---

## 📊 Screen 4: Risk Assessment Questionnaire

**URL:** `/risk-assessment`

**Layout:**
```
┌─────────────────────────────────────┐
│ ← Portfolio Advisor        user@... │
│─────────────────────────────────────│
│                                     │
│  Risk Assessment                    │
│  Answer these questions to determine│
│  your investment risk profile       │
│                                     │
│  [Progress: Q1-Q2-Q3-Q4-Q5-Q6-Q7-Q8]│
│                                     │
│  1. What is your investment time    │
│     horizon?                        │
│                                     │
│  ○ Less than 3 years               │
│  ○ 3-5 years                       │
│  ○ 5-10 years                      │
│  ○ 10-20 years                     │
│  ○ More than 20 years              │
│                                     │
│  [Back]                [Next →]     │
└─────────────────────────────────────┘
```

**Questions (8 total):**
1. Investment time horizon
2. Reaction to 20% portfolio loss
3. Primary investment goal
4. Loss tolerance percentage
5. Investment experience level
6. Emergency fund status
7. Income stability
8. Market knowledge

**After Completion:**
- Shows success message
- Calculates risk score (0-100)
- Assigns category (Conservative to Aggressive)
- Redirects to Portfolio page

---

## 🏠 Screen 5: Dashboard (Main View)

**URL:** `/`

**Layout:**
```
┌─────────────────────────────────────┐
│ ☰ Portfolio Advisor    user@...🚪 │
│─────────────────────────────────────│
│ Dashboard                           │
│ Welcome to your portfolio dashboard │
│                                     │
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐│
│ │$100K │ │ 7.0% │ │Moder-│ │ 0.85 ││
│ │Value │ │Return│ │ ate  │ │Sharpe││
│ └──────┘ └──────┘ └──────┘ └──────┘│
│                                     │
│ ┌──────────────┐ ┌─────────────────┐│
│ │ Asset        │ │ Market Overview ││
│ │ Allocation   │ │                 ││
│ │              │ │ S&P 500   +1.2% ││
│ │  [PIE CHART] │ │ NASDAQ    +0.8% ││
│ │              │ │ Dow Jones +0.5% ││
│ │ • Stocks 60% │ │ Russell   +1.0% ││
│ │ • Bonds  30% │ │                 ││
│ │ • Alts    8% │ │                 ││
│ │ • Cash    2% │ │                 ││
│ └──────────────┘ └─────────────────┘│
│                                     │
│ Quick Actions                       │
│ [Take Risk Assessment]              │
│ [View Portfolio Details]            │
│ [Run Scenario Analysis]             │
└─────────────────────────────────────┘
```

**Left Sidebar (Drawer):**
```
┌──────────────┐
│ Portfolio    │
│ Advisor      │
├──────────────┤
│ ⊞ Dashboard  │ ← Selected
│ ❓ Risk Ass. │
│ 💼 Portfolio │
│ 📊 Scenarios │
└──────────────┘
```

**Features:**
- 4 stat cards at top (Portfolio Value, Expected Return, Risk Level, Sharpe Ratio)
- Interactive pie chart (hover shows details)
- Real-time market data updates
- Mobile responsive - stacks vertically on phone

---

## 💼 Screen 6: Portfolio Recommendation

**URL:** `/portfolio`

**Layout:**
```
┌─────────────────────────────────────┐
│ Portfolio Recommendation            │
│ [MODERATE CHIP]           [🔄Refresh]│
│                                     │
│ ┌──────────────┐ ┌─────────────────┐│
│ │ Expected     │ │                 ││
│ │ Performance  │ │  Asset          ││
│ │              │ │  Allocation     ││
│ │ Return: 7.0% │ │                 ││
│ │ Vol:   12.0% │ │  [PIE CHART]    ││
│ │ Sharpe: 0.85 │ │                 ││
│ └──────────────┘ └─────────────────┘│
│                                     │
│ Recommended Holdings                │
│ ┌───────────────────────────────────┐│
│ │Symbol│Name    │Asset│Alloc│Amount││
│ ├───────────────────────────────────┤│
│ │VTI   │Vanguard│Equity│30% │$30K  ││
│ │VXUS  │Intl Stk│Equity│18% │$18K  ││
│ │VO    │Mid Cap │Equity│ 6% │ $6K  ││
│ │VB    │Sm Cap  │Equity│ 6% │ $6K  ││
│ │BND   │Bonds   │Fixed │21% │$21K  ││
│ │VCIT  │Corp Bnd│Fixed │ 9% │ $9K  ││
│ │VNQ   │REITs   │Alt   │ 5% │ $5K  ││
│ │GLD   │Gold    │Alt   │ 3% │ $3K  ││
│ │CASH  │Cash/MM │Cash  │ 2% │ $2K  ││
│ └───────────────────────────────────┘│
│                                     │
│ Recommendation Rationale            │
│ • Strategy: Modern Portfolio Theory │
│ • Balanced risk/return for moderate │
│ • Diversified across asset classes  │
│ • Rebalance quarterly              │
└─────────────────────────────────────┘
```

**Mobile View:**
- Holdings table scrolls horizontally
- Charts resize to full width
- All information accessible via scrolling

---

## 🎲 Screen 7: Scenario Analysis

**URL:** `/scenarios`

**Layout:**
```
┌─────────────────────────────────────┐
│ Scenario Analysis           [Clear] │
│ Test portfolio under market condtns │
│                                     │
│ [Predefined] [Custom] [Monte Carlo] │
│                                     │
│ Select Scenario ▼                   │
│ ┌───────────────────────────────────┐│
│ │ Market Crash (-30%)               ││
│ │ Recession                         ││
│ │ High Inflation (+5%)              ││
│ │ Rising Interest Rates (+2%)       ││
│ │ Bull Market (+20%)                ││
│ └───────────────────────────────────┘│
│                                     │
│ [▶ Run Scenario]                    │
│                                     │
│ ─── RESULTS ───                     │
│                                     │
│ Scenario Results Table              │
│ ┌───────────────────────────────────┐│
│ │Scenario     │Value  │Gain/Loss│  ││
│ ├───────────────────────────────────┤│
│ │Market Crash │$70K   │-$30K -30%│  ││
│ │Recovery: 30 months               ││
│ │                                  ││
│ │Recommendations:                  ││
│ │• Consider rebalancing            ││
│ │• Ensure emergency fund adequate  ││
│ └───────────────────────────────────┘│
└─────────────────────────────────────┘
```

**Custom Scenario Tab:**
```
│ Stock Market Return (%)  [ -30  ]   │
│ Bond Market Return (%)   [  5   ]   │
│ [▶ Run Custom Scenario]             │
```

**Monte Carlo Tab:**
```
│ Number of Simulations   [ 1000  ]   │
│ Time Horizon (years)    [  10   ]   │
│ [▶ Run Simulation]                  │
│                                     │
│ ─── RESULTS ───                     │
│                                     │
│ Expected Value:    $250,000         │
│ Best Case (90th):  $380,000         │
│ Worst Case (10th): $150,000         │
│ Positive Return:   85%              │
│                                     │
│ [BAR CHART showing percentiles]     │
```

---

## 📱 Mobile-Specific Features

### Navigation
- **Hamburger Menu (☰):** Tap to open sidebar drawer
- **Swipe Gesture:** Swipe from left edge to open menu
- **Bottom Navigation:** Easy thumb reach on Pixel 10

### Touch Interactions
- **Charts:** Tap to see data points
- **Tables:** Horizontal scroll with finger swipe
- **Forms:** Native keyboard with proper input types
- **Buttons:** Large touch targets (48px minimum)

### Responsive Design
- All content stacks vertically on mobile
- Cards take full width
- Text sizes adjust for readability
- Charts resize to fit screen
- No horizontal overflow

---

## 🎨 Color Scheme

- **Primary Blue:** #1976d2 (buttons, highlights)
- **Success Green:** #4caf50 (positive returns)
- **Error Red:** #f44336 (losses, errors)
- **Warning Orange:** #ff9800 (risk indicators)
- **Purple:** #9c27b0 (metrics)

**Chart Colors:**
- Stocks: #0088FE (Blue)
- Bonds: #00C49F (Green)
- Alternatives: #FFBB28 (Yellow)
- Cash: #FF8042 (Orange)

---

## 📸 How to Take Screenshots on Pixel 10

1. **Power + Volume Down** - Hold both buttons
2. **Screenshots auto-save** to Photos app
3. **Share via:** Google Photos, Drive, or Messages

## 🚀 Getting Started Checklist

- [ ] Update `vite.config.js` (already done ✓)
- [ ] Find your computer's IP address
- [ ] Start backend on port 8000
- [ ] Start frontend on port 5173
- [ ] Connect phone to same WiFi
- [ ] Open browser on phone
- [ ] Navigate to `http://YOUR_IP:5173`
- [ ] Register an account
- [ ] Complete onboarding
- [ ] Take risk assessment
- [ ] View your portfolio!

---

## 💡 Tips for Best Mobile Experience

1. **Use Chrome** on Android for best compatibility
2. **Add to Home Screen** for app-like experience:
   - Chrome menu → "Add to Home Screen"
   - Creates icon on your Pixel 10
3. **Landscape Mode** works great for charts
4. **Dark Mode** - Browser will respect system setting
5. **Touch Zoom** - Pinch to zoom on charts

Enjoy exploring your financial portfolio on your Pixel 10! 📱💰
