```python
#!/usr/bin/env python3
"""
Hacktoberfest Trading Simulator 2025
Single-file project for backtesting trading strategies on synthetic price data.
"""

import argparse
import random
import statistics
from typing import List, Tuple

# ----------------- Data Generator -----------------
def generate_price_series(days: int, start: float = 100.0) -> List[float]:
    """Generate synthetic stock prices using random walk."""
    prices = [start]
    for _ in range(days - 1):
        change = random.uniform(-2, 2)  # ±2% daily move
        prices.append(prices[-1] * (1 + change / 100))
    return prices

# ----------------- Strategy -----------------
def sma_crossover(prices: List[float], short: int = 10, long: int = 30) -> List[int]:
    """Simple Moving Average Crossover strategy.
    Returns a list of signals: 1 = buy, -1 = sell, 0 = hold
    """
    signals = [0] * len(prices)
    for i in range(long, len(prices)):
        short_avg = statistics.mean(prices[i - short:i])
        long_avg = statistics.mean(prices[i - long:i])
        if short_avg > long_avg:
            signals[i] = 1
        elif short_avg < long_avg:
            signals[i] = -1
    return signals

# ----------------- Backtesting -----------------
def backtest(prices: List[float], signals: List[int], initial_cash: float = 10000) -> dict:
    cash = initial_cash
    position = 0  # number of shares
    trades = []
    balance_history = []

    for i in range(len(prices)):
        price = prices[i]
        signal = signals[i]

        # Execute trades
        if signal == 1 and cash > 0:  # Buy
            position = cash / price
            cash = 0
            trades.append(("BUY", price, i))
        elif signal == -1 and position > 0:  # Sell
            cash = position * price
            position = 0
            trades.append(("SELL", price, i))

        balance = cash + position * price
        balance_history.append(balance)

    final_balance = cash + position * prices[-1]

    # Metrics
    trade_results = []
    for i in range(1, len(trades), 2):
        buy_price = trades[i-1][1]
        sell_price = trades[i][1]
        trade_results.append((sell_price - buy_price) / buy_price)

    win_rate = sum(1 for r in trade_results if r > 0) / len(trade_results) * 100 if trade_results else 0
    max_drawdown = min((balance - max(balance_history[:i+1])) / max(balance_history[:i+1]) * 100
                       for i, balance in enumerate(balance_history)) if balance_history else 0

    return {
        "initial": initial_cash,
        "final": round(final_balance, 2),
        "trades": len(trade_results),
        "win_rate": round(win_rate, 2),
        "max_drawdown": round(max_drawdown, 2)
    }

# ----------------- CLI -----------------
def main():
    parser = argparse.ArgumentParser(description="Hacktoberfest Trading Simulator 2025")
    parser.add_argument("--strategy", choices=["sma"], default="sma", help="Trading strategy")
    parser.add_argument("--cash", type=float, default=10000, help="Initial cash")
    parser.add_argument("--days", type=int, default=200, help="Number of days for simulation")
    args = parser.parse_args()

    prices = generate_price_series(args.days)

    if args.strategy == "sma":
        signals = sma_crossover(prices)
        results = backtest(prices, signals, args.cash)
        print("\n📈 Hacktoberfest Trading Simulator 2025")
        print(f"Strategy: SMA Crossover")
        print(f"Initial Cash: {results['initial']}")
        print(f"Final Balance: {results['final']}")
        print(f"Total Trades: {results['trades']}")
        print(f"Win Rate: {results['win_rate']}%")
        print(f"Max Drawdown: {results['max_drawdown']}%")

if __name__ == "__main__":
    main()
