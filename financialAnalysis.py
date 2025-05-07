import yfinance as yf
import matplotlib
import pandas as pd
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.risk_models import risk_matrix
from pypfopt.expected_returns import mean_historical_return
from pypfopt.plotting import plot_efficient_frontier
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

# 10 diversified tech + AI stock tickers
tickers = ['AAPL', 'MSFT', 'NVDA', 'TSLA', 'GOOGL', 'AMD', 'META', 'TSM', 'ASML', 'INTC']

start_date = '2015-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')

# Download stock data
data = yf.download(tickers, start=start_date, end=end_date)['Close']
data = data.dropna()

# Price plot
plt.figure(figsize=(12, 8))
for ticker in tickers:
    plt.plot(data[ticker], label=ticker)
plt.title("Stock Prices (2015–Present)")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig('price_history.png')
plt.show()

# Correlation heatmap
daily_returns = data.pct_change().dropna()
correlation_matrix = daily_returns.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title("Daily Return Correlation (2015–Present)")
plt.tight_layout()
plt.savefig('correlation_map.png')
plt.show()

# PyPortfolioOpt expected return and covariance
mu = mean_historical_return(data)
S = risk_matrix(data)

# Optimization: Max Sharpe ratio
ef = EfficientFrontier(mu, S)
#ef.add_objective(lambda w: cp.norm1(w))  # L1 regularization using CVXPY
ef.add_constraint(lambda w: w <= 0.19)  # No more than 14% in any one stock
ef.add_constraint(lambda w: w >= 0.02)
weights = ef.max_sharpe()
cleaned_weights = ef.clean_weights()
print("Optimized Weights:\n", cleaned_weights)

# Performance report
expected_return, volatility, sharpe_ratio = ef.portfolio_performance(verbose=True)

# Plot Efficient Frontier
fig, ax = plt.subplots(figsize=(10, 7))
ef_plot = EfficientFrontier(mu, S)  # New instance just for plotting
plot_efficient_frontier(ef_plot, ax=ax, show_assets=True)
plt.title("Efficient Frontier (PyPortfolioOpt)")
plt.tight_layout()
plt.savefig("efficient_frontier_pypfopt.png")
plt.show()

# Discrete allocation (simulate real investment of $20,000)
latest_prices = get_latest_prices(data)
da = DiscreteAllocation(cleaned_weights, latest_prices, total_portfolio_value=20000)
allocation, leftover = da.lp_portfolio()
print("\nDiscrete Allocation (approx. $20,000):")
print(allocation)
print(f"Unallocated Cash: ${leftover:.2f}")


# Pie chart of optimal weights
plt.figure(figsize=(8, 8))
labels = []
sizes = []

for stock, weight in cleaned_weights.items():
    if weight > 0.01:  # Only show meaningful weights (>1%)
        labels.append(stock)
        sizes.append(weight)

plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title('Optimized Portfolio Allocation')
plt.tight_layout()
plt.savefig("optimal_portfolio_piechart.png")
plt.show()


# Create a table from discrete allocation
allocation_df = pd.DataFrame(list(allocation.items()), columns=['Ticker', 'Shares'])
allocation_df['Price per Share'] = allocation_df['Ticker'].apply(lambda x: latest_prices[x])
allocation_df['Total Value'] = allocation_df['Shares'] * allocation_df['Price per Share']
allocation_df = allocation_df.sort_values(by='Total Value', ascending=False).reset_index(drop=True)

# Add unallocated cash as a row
allocation_df.loc[len(allocation_df.index)] = ['CASH', '', '', leftover]

# Display the table
print("\nFinal Investment Breakdown:")
print(allocation_df.to_string(index=False))

(allocation_df.to_csv('portfolio_allocation_summary.csv', index=False))