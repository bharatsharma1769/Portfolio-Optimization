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
* One-day we
