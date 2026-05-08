# Portfolio-Optimization for Algorithmic Trading

A Python-based algorithmic trading research pipeline for ETF rotation, portfolio construction, and risk-aware strategy evaluation. The project combines machine learning signal generation, realistic walk-forward backtesting, regime-aware portfolio allocation, transaction-cost modelling, Monte Carlo robustness analysis, and historical stress testing.

This project was developed as a final-year project with emphasis on engineering rigor, reproducible research workflow, and practical evaluation of trading strategies rather than purely maximizing historical returns.

---

## Project Overview

The objective of this project is to design and evaluate a systematic ETF rotation framework that ranks a diversified universe of exchange-traded funds and constructs long-only portfolios under realistic trading assumptions.

The core workflow is:

1. Build a diversified multi-asset ETF universe.
2. Engineer technical and risk-based features from historical market data.
3. Construct forward-return targets for cross-sectional asset ranking.
4. Train a walk-forward LightGBM ranking model.
5. Convert out-of-sample model scores into portfolio allocations.
6. Backtest strategies with transaction costs, turnover control, and volatility targeting.
7. Compare different portfolio construction methods.
8. Evaluate robustness through Monte Carlo simulations and stress testing.

---

## Key Features

* End-to-end Python research pipeline using Jupyter notebooks and reusable helper modules.
* Multi-asset ETF universe covering equities, fixed income, commodities, gold, REITs, and defensive sectors.
* Cross-sectional machine learning model for ETF ranking using LightGBM.
* Strict walk-forward training, validation, and out-of-sample testing framework.
* Regime-aware portfolio construction using SPY trend filters.
* Multiple allocation methods:

  * Equal Weight
  * Inverse Volatility
  * Mean-Variance Optimization
  * CVaR Optimization
  * Hybrid Mean-Variance + CVaR
* Realistic backtesting mechanics:

  * Discrete rebalancing
  * Transaction costs
  * Turnover measurement
  * Volatility targeting
  * Weight shifting to avoid look-ahead bias
* Robustness analysis through:

  * Bootstrap Monte Carlo simulations
  * Random portfolio clouds
  * Input-uncertainty simulations
  * Historical stress-period testing
  * Static asset-class shock scenarios
* Transaction-cost sensitivity analysis across optimistic, base, and stressed assumptions.

---

## Methodology

### 1. ETF Universe

The strategy uses a diversified ETF universe across asset classes. The universe includes equity index ETFs, defensive sector ETFs, fixed income ETFs, gold, commodities, and REIT exposure.

The goal is not to predict a single asset in isolation, but to rank ETFs cross-sectionally and rotate into the most attractive assets under each market regime.

---

### 2. Feature Engineering

Features are generated from historical price and return data. They include common technical, trend, momentum, volatility, and mean-reversion indicators.

Examples include:

* Momentum over multiple lookback windows
* Rolling volatility
* Moving-average trend signals
* Relative strength indicators
* Bollinger Band features
* ATR-style volatility measures
* Cross-sectional standardized features

Features are aligned carefully to avoid look-ahead bias.

---

### 3. Target Construction

The target is based on point-to-point forward returns over a short holding horizon. Forward returns are transformed into cross-sectional ranking targets so that the model learns relative attractiveness across ETFs rather than absolute return prediction.

The final version uses robust cross-sectional normalization with Median Absolute Deviation (MAD), reducing the influence of extreme outliers.

---

### 4. Signal Model

A LightGBM model is trained to generate cross-sectional ETF scores.

The model is evaluated using a strict walk-forward framework:

* Rolling training windows
* Validation period for early stopping
* Yearly out-of-sample testing
* No future data leakage
* Signal evaluation aligned with the final top-k portfolio selection rule

The model output is not treated as a direct return forecast. Instead, it is used as a ranking signal for ETF selection.

---

### 5. Regime-Aware Portfolio Construction

The portfolio layer uses a regime-aware allocation framework based on SPY trend filters.

The regimes are:

| Regime         | Condition                                         | Portfolio Behaviour                  |
| -------------- | ------------------------------------------------- | ------------------------------------ |
| Risk-Off       | SPY below 100-day moving average                  | Defensive basket selection           |
| Normal Risk-On | SPY above 100-day moving average                  | Balanced equity/defensive allocation |
| Strong Bull    | SPY above both 50-day and 100-day moving averages | More equity-focused allocation       |

Rebalancing frequency and holding periods are adjusted by regime:

| Regime         | Holding Period  |
| -------------- | --------------- |
| Risk-Off       | 3 trading days  |
| Normal Risk-On | 5 trading days  |
| Strong Bull    | 10 trading days |

A trade-buffer mechanism is used to reduce unnecessary turnover when the selected basket has not changed meaningfully.

---

## Portfolio Construction Methods

The project compares several portfolio allocation methods.

### Equal Weight

Allocates capital equally across selected ETFs. This acts as a simple and robust baseline.

### Inverse Volatility

Allocates more weight to lower-volatility assets and less weight to higher-volatility assets. In the project results, this method is generally the most stable and performs strongly on a risk-adjusted basis.

### Mean-Variance Optimization

Uses estimated expected returns and covariance to optimize portfolio weights. While theoretically attractive, the method can be unstable and sensitive to estimation noise.

### CVaR Optimization

Uses Conditional Value at Risk to incorporate downside-risk awareness into portfolio construction.

### Hybrid Mean-Variance + CVaR

Combines return-risk optimization with downside-risk constraints. This method is included as an extension, though simpler allocators often prove more robust in practice.

---

## Backtesting Design

The backtest is designed to reflect practical implementation constraints.

Key assumptions include:

* Long-only ETF portfolios
* Discrete rebalancing
* Out-of-sample model scores only
* One-day weweight shifting to prevent look-ahead bias
Transaction costs applied to turnover
Volatility targeting to a fixed annualized risk level
Performance comparison against a full-universe equal-weight buy-and-hold benchmark

The benchmark is intentionally simple and transparent. It provides a diversified passive reference point rather than an optimized trading strategy.

Transaction Cost Assumptions

The base transaction-cost assumption is 12 basis points per unit of turnover.

This is treated as a conservative all-in estimate covering:

Commissions
Bid-ask spread crossing
Slippage
Implementation friction

A sensitivity analysis is included using:

Scenario	Cost Assumption
Optimistic	8 bps
Base	12 bps
Stressed	25 bps

The purpose is not to claim broker-exact execution costs, but to demonstrate that results are evaluated under multiple implementation-cost assumptions.

Monte Carlo Robustness Analysis

The Monte Carlo notebook evaluates whether strategy conclusions are robust beyond a single historical backtest path.

It includes:

Bootstrap simulations of realized out-of-sample strategy returns.
Random long-only portfolio clouds for comparison against simple reference allocators.
Input-uncertainty simulations for Equal Weight, Inverse Volatility, and Mean-Variance portfolios.

The results show that Mean-Variance optimization is more sensitive to estimation noise, while Equal Weight and Inverse Volatility are more stable.

Stress Testing

The stress-testing notebook evaluates performance during historical and hypothetical adverse scenarios.

Historical stress periods include:

2018 Q4 market selloff
2020 COVID crash
2022 rate shock

Static shock scenarios test portfolio sensitivity to asset-class-level shocks, such as equity drawdowns and bond selloffs.

The stress tests help identify whether each allocation method is exposed primarily to equity risk, bond risk, or broader cross-asset stress.

Main Findings

The main findings are:

The LightGBM signal is useful as a ranking input, but the raw predictive edge is modest.
Portfolio construction and risk management materially affect final performance.
Regime-aware rebalancing improves practical strategy behaviour by reducing overtrading.
Simpler allocation methods, especially Inverse Volatility, are more robust than complex optimizers.
Mean-Variance optimization can produce unstable and concentrated weights under input uncertainty.
The passive equal-weight full-universe benchmark remains difficult to outperform consistently, especially across strong equity bull-market periods.
Stress testing and Monte Carlo analysis are essential for understanding robustness beyond headline backtest metrics.
