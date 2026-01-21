import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from pypfopt import EfficientFrontier, risk_models, expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation
from app.services.market_data_service import MarketDataService


class PortfolioRecommendationEngine:
    """Engine for generating portfolio recommendations"""

    # Risk profiles and corresponding target allocations
    RISK_PROFILES = {
        "conservative": {
            "stocks": 30,
            "bonds": 60,
            "alternatives": 5,
            "cash": 5,
            "expected_return": 0.05,
            "expected_volatility": 0.08,
        },
        "moderate_conservative": {
            "stocks": 45,
            "bonds": 45,
            "alternatives": 7,
            "cash": 3,
            "expected_return": 0.06,
            "expected_volatility": 0.10,
        },
        "moderate": {
            "stocks": 60,
            "bonds": 30,
            "alternatives": 8,
            "cash": 2,
            "expected_return": 0.07,
            "expected_volatility": 0.12,
        },
        "moderate_aggressive": {
            "stocks": 75,
            "bonds": 15,
            "alternatives": 9,
            "cash": 1,
            "expected_return": 0.08,
            "expected_volatility": 0.15,
        },
        "aggressive": {
            "stocks": 85,
            "bonds": 5,
            "alternatives": 10,
            "cash": 0,
            "expected_return": 0.09,
            "expected_volatility": 0.18,
        },
    }

    # ETF recommendations by asset class
    ETF_RECOMMENDATIONS = {
        "us_large_cap": {"symbol": "VTI", "name": "Vanguard Total Stock Market ETF"},
        "us_mid_cap": {"symbol": "VO", "name": "Vanguard Mid-Cap ETF"},
        "us_small_cap": {"symbol": "VB", "name": "Vanguard Small-Cap ETF"},
        "international": {"symbol": "VXUS", "name": "Vanguard Total International Stock ETF"},
        "emerging": {"symbol": "VWO", "name": "Vanguard Emerging Markets ETF"},
        "bonds_total": {"symbol": "BND", "name": "Vanguard Total Bond Market ETF"},
        "bonds_treasury": {"symbol": "GOVT", "name": "iShares U.S. Treasury Bond ETF"},
        "bonds_corporate": {"symbol": "VCIT", "name": "Vanguard Intermediate-Term Corporate Bond ETF"},
        "reits": {"symbol": "VNQ", "name": "Vanguard Real Estate ETF"},
        "commodities": {"symbol": "DBC", "name": "Invesco DB Commodity Index Tracking Fund"},
        "gold": {"symbol": "GLD", "name": "SPDR Gold Trust"},
    }

    @staticmethod
    def calculate_risk_score(responses: Dict[str, str]) -> Tuple[int, str]:
        """Calculate risk score from questionnaire responses"""
        score = 0

        # Question 1: Time horizon
        horizon_scores = {
            "less_than_3": 10,
            "3_to_5": 20,
            "5_to_10": 35,
            "10_to_20": 50,
            "more_than_20": 65,
        }
        score += horizon_scores.get(responses.get("question_1", "5_to_10"), 35)

        # Question 2: Reaction to loss
        loss_scores = {
            "sell_all": 5,
            "sell_some": 15,
            "do_nothing": 30,
            "buy_more": 50,
        }
        score += loss_scores.get(responses.get("question_2", "do_nothing"), 30)

        # Question 3: Primary goal
        goal_scores = {
            "preservation": 10,
            "income": 20,
            "balanced": 35,
            "growth": 50,
            "aggressive_growth": 65,
        }
        score += goal_scores.get(responses.get("question_3", "balanced"), 35)

        # Question 4: Loss tolerance
        tolerance_scores = {
            "0_to_5": 10,
            "5_to_10": 25,
            "10_to_20": 40,
            "20_plus": 60,
        }
        score += tolerance_scores.get(responses.get("question_4", "10_to_20"), 40)

        # Question 5: Experience
        experience_scores = {
            "none": 10,
            "beginner": 20,
            "intermediate": 35,
            "advanced": 50,
        }
        score += experience_scores.get(responses.get("question_5", "intermediate"), 35)

        # Question 6: Emergency savings
        savings_scores = {
            "no": 5,
            "partial": 15,
            "yes": 25,
        }
        score += savings_scores.get(responses.get("question_6", "yes"), 25)

        # Question 7: Income stability
        income_scores = {
            "unstable": 10,
            "somewhat_stable": 20,
            "stable": 30,
        }
        score += income_scores.get(responses.get("question_7", "stable"), 30)

        # Question 8: Market knowledge
        knowledge_scores = {
            "low": 10,
            "moderate": 25,
            "high": 40,
        }
        score += knowledge_scores.get(responses.get("question_8", "moderate"), 25)

        # Normalize to 0-100
        normalized_score = min(100, max(0, int(score / 3.4)))

        # Determine category
        if normalized_score < 25:
            category = "conservative"
        elif normalized_score < 45:
            category = "moderate_conservative"
        elif normalized_score < 65:
            category = "moderate"
        elif normalized_score < 80:
            category = "moderate_aggressive"
        else:
            category = "aggressive"

        return normalized_score, category

    @staticmethod
    def generate_recommendation(
        risk_category: str,
        investable_amount: float,
        preferences: Dict = None
    ) -> Dict:
        """Generate portfolio recommendation based on risk profile"""

        # Get base allocation from risk profile
        base_allocation = PortfolioRecommendationEngine.RISK_PROFILES.get(
            risk_category, PortfolioRecommendationEngine.RISK_PROFILES["moderate"]
        )

        # Build portfolio holdings
        holdings = []

        # Stocks allocation
        stock_pct = base_allocation["stocks"] / 100
        if stock_pct > 0:
            # Split stocks: 50% US Large, 20% International, 15% Mid, 15% Small
            holdings.append({
                "symbol": "VTI",
                "name": "Vanguard Total Stock Market ETF",
                "asset_class": "equity",
                "allocation_pct": stock_pct * 0.50,
                "amount": investable_amount * stock_pct * 0.50,
            })
            holdings.append({
                "symbol": "VXUS",
                "name": "Vanguard Total International Stock ETF",
                "asset_class": "equity",
                "allocation_pct": stock_pct * 0.30,
                "amount": investable_amount * stock_pct * 0.30,
            })
            holdings.append({
                "symbol": "VO",
                "name": "Vanguard Mid-Cap ETF",
                "asset_class": "equity",
                "allocation_pct": stock_pct * 0.10,
                "amount": investable_amount * stock_pct * 0.10,
            })
            holdings.append({
                "symbol": "VB",
                "name": "Vanguard Small-Cap ETF",
                "asset_class": "equity",
                "allocation_pct": stock_pct * 0.10,
                "amount": investable_amount * stock_pct * 0.10,
            })

        # Bonds allocation
        bond_pct = base_allocation["bonds"] / 100
        if bond_pct > 0:
            # Split bonds: 70% Total Bond, 30% Corporate
            holdings.append({
                "symbol": "BND",
                "name": "Vanguard Total Bond Market ETF",
                "asset_class": "fixed_income",
                "allocation_pct": bond_pct * 0.70,
                "amount": investable_amount * bond_pct * 0.70,
            })
            holdings.append({
                "symbol": "VCIT",
                "name": "Vanguard Intermediate-Term Corporate Bond ETF",
                "asset_class": "fixed_income",
                "allocation_pct": bond_pct * 0.30,
                "amount": investable_amount * bond_pct * 0.30,
            })

        # Alternatives allocation
        alt_pct = base_allocation["alternatives"] / 100
        if alt_pct > 0:
            # Split alternatives: 60% REITs, 40% Gold
            holdings.append({
                "symbol": "VNQ",
                "name": "Vanguard Real Estate ETF",
                "asset_class": "alternatives",
                "allocation_pct": alt_pct * 0.60,
                "amount": investable_amount * alt_pct * 0.60,
            })
            holdings.append({
                "symbol": "GLD",
                "name": "SPDR Gold Trust",
                "asset_class": "alternatives",
                "allocation_pct": alt_pct * 0.40,
                "amount": investable_amount * alt_pct * 0.40,
            })

        # Cash allocation
        cash_pct = base_allocation["cash"] / 100
        if cash_pct > 0:
            holdings.append({
                "symbol": "CASH",
                "name": "Cash or Money Market",
                "asset_class": "cash",
                "allocation_pct": cash_pct,
                "amount": investable_amount * cash_pct,
            })

        # Get current prices and calculate shares
        for holding in holdings:
            if holding["symbol"] != "CASH":
                price = MarketDataService.get_current_price(holding["symbol"])
                if price:
                    holding["current_price"] = price
                    holding["shares"] = holding["amount"] / price
                else:
                    holding["current_price"] = 0
                    holding["shares"] = 0

        # Calculate portfolio metrics
        sharpe_ratio = (base_allocation["expected_return"] - 0.02) / base_allocation["expected_volatility"]

        return {
            "recommended_allocation": {
                "stocks": base_allocation["stocks"],
                "bonds": base_allocation["bonds"],
                "alternatives": base_allocation["alternatives"],
                "cash": base_allocation["cash"],
            },
            "recommended_holdings": holdings,
            "expected_return": base_allocation["expected_return"],
            "expected_volatility": base_allocation["expected_volatility"],
            "sharpe_ratio": round(sharpe_ratio, 2),
            "strategy": "Modern Portfolio Theory",
            "risk_category": risk_category,
            "rationale": {
                "allocation_explanation": f"This {risk_category} portfolio balances risk and return based on your profile.",
                "diversification": "Holdings are diversified across asset classes, sectors, and geographies.",
                "rebalancing": "Recommend quarterly rebalancing to maintain target allocation.",
            },
        }


class ScenarioAnalysisEngine:
    """Engine for scenario analysis and stress testing"""

    PREDEFINED_SCENARIOS = {
        "market_crash": {
            "name": "Market Crash (-30%)",
            "stock_return": -0.30,
            "bond_return": 0.05,
            "alternatives_return": -0.15,
            "cash_return": 0.01,
        },
        "recession": {
            "name": "Recession",
            "stock_return": -0.15,
            "bond_return": 0.03,
            "alternatives_return": -0.10,
            "cash_return": 0.01,
        },
        "high_inflation": {
            "name": "High Inflation (+5%)",
            "stock_return": 0.05,
            "bond_return": -0.10,
            "alternatives_return": 0.15,
            "cash_return": -0.03,
        },
        "rising_rates": {
            "name": "Rising Interest Rates (+2%)",
            "stock_return": -0.05,
            "bond_return": -0.08,
            "alternatives_return": 0.02,
            "cash_return": 0.03,
        },
        "bull_market": {
            "name": "Bull Market (+20%)",
            "stock_return": 0.20,
            "bond_return": 0.02,
            "alternatives_return": 0.10,
            "cash_return": 0.01,
        },
    }

    @staticmethod
    def run_scenario(
        portfolio_value: float,
        allocation: Dict[str, float],
        scenario_name: str = None,
        custom_returns: Dict[str, float] = None
    ) -> Dict:
        """Run scenario analysis on portfolio"""

        if scenario_name and scenario_name in ScenarioAnalysisEngine.PREDEFINED_SCENARIOS:
            scenario = ScenarioAnalysisEngine.PREDEFINED_SCENARIOS[scenario_name]
            returns = {
                "stocks": scenario["stock_return"],
                "bonds": scenario["bond_return"],
                "alternatives": scenario["alternatives_return"],
                "cash": scenario["cash_return"],
            }
            name = scenario["name"]
        elif custom_returns:
            returns = custom_returns
            name = "Custom Scenario"
        else:
            returns = {"stocks": 0, "bonds": 0, "alternatives": 0, "cash": 0}
            name = "No Change"

        # Calculate impact on portfolio
        new_value = 0
        for asset_class, pct in allocation.items():
            if asset_class in returns:
                asset_value = portfolio_value * (pct / 100)
                new_asset_value = asset_value * (1 + returns[asset_class])
                new_value += new_asset_value

        gain_loss = new_value - portfolio_value
        gain_loss_pct = (gain_loss / portfolio_value * 100) if portfolio_value > 0 else 0

        # Estimate recovery time (simplified)
        recovery_months = None
        if gain_loss < 0:
            # Assume 1% monthly recovery
            recovery_months = int(abs(gain_loss_pct))

        recommendations = []
        if gain_loss_pct < -10:
            recommendations.append("Consider rebalancing to take advantage of lower prices")
            recommendations.append("Ensure emergency fund is adequate before investing more")
        elif gain_loss_pct > 15:
            recommendations.append("Consider taking some profits and rebalancing")
            recommendations.append("Review if portfolio has drifted from target allocation")

        return {
            "scenario_name": name,
            "projected_value": round(new_value, 2),
            "expected_gain_loss": round(gain_loss, 2),
            "expected_gain_loss_pct": round(gain_loss_pct, 2),
            "recovery_time_months": recovery_months,
            "recommendations": recommendations,
        }

    @staticmethod
    def monte_carlo_simulation(
        portfolio_value: float,
        expected_return: float,
        volatility: float,
        years: int,
        num_simulations: int = 1000,
        monthly_contribution: float = 0
    ) -> Dict:
        """Run Monte Carlo simulation for portfolio projections"""

        np.random.seed(42)

        # Convert annual metrics to monthly
        monthly_return = expected_return / 12
        monthly_volatility = volatility / np.sqrt(12)
        months = years * 12

        # Run simulations
        final_values = []

        for _ in range(num_simulations):
            value = portfolio_value
            for month in range(months):
                # Add contribution
                value += monthly_contribution

                # Generate random return
                random_return = np.random.normal(monthly_return, monthly_volatility)
                value = value * (1 + random_return)

            final_values.append(value)

        final_values = np.array(final_values)

        # Calculate percentiles
        percentiles = {
            "10th": float(np.percentile(final_values, 10)),
            "25th": float(np.percentile(final_values, 25)),
            "50th": float(np.percentile(final_values, 50)),
            "75th": float(np.percentile(final_values, 75)),
            "90th": float(np.percentile(final_values, 90)),
        }

        return {
            "simulations": num_simulations,
            "percentiles": percentiles,
            "expected_value": float(np.mean(final_values)),
            "worst_case": float(np.min(final_values)),
            "best_case": float(np.max(final_values)),
            "probability_of_positive_return": float(np.sum(final_values > portfolio_value) / num_simulations),
        }
