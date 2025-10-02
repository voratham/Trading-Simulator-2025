# Trading-Simulator-2025

A single-file Python project for simulating trading strategies with mock price data.  
Perfect for Hacktoberfest contributors — add new strategies, risk metrics, or visualization features!

**Repo name:** `hacktoberfest-trading-simulator-2025`  
**File name:** `trading_simulator.py`

---

## Features
- Generates synthetic market price data
- Implements a sample Moving Average Crossover strategy
- Backtests trading signals
- Calculates simple performance metrics (profit, win-rate, max drawdown)
- CLI-based usage — extendable with more strategies

---

## Quick Start

```bash
python trading_simulator.py --strategy sma --cash 10000 --days 200
