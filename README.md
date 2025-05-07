# financialAnalysis

This project models a portfolio optimization scenario for a 23-year-old client looking to invest **$20,000** in a **long-term (10+ year)** stock portfolio, with a focus on **tech and AI growth stocks**. Using historical market data, Python-based analysis, and modern portfolio theory, the project identifies an optimal stock allocation that balances **risk and return** according to the client's investment profile. The code is written to be flexible and dynamic; the data reflected in the presentation represents data gathered from live market conditions as of May 7, 2025, and dating back to January 1, 2015, however the code is designed to auto-update based on the run date. Stock ticker symbols can also be replaced, added, or removed as needed by the user to analyze a different sector of the market. 

**Tools & Libraries Used**
- **Python** – Core language for all analysis
- **yfinance** – Real-time stock price and historical data collection
- **pandas / numpy** – Data wrangling and statistical analysis
- **matplotlib / seaborn** – Data visualization (line charts, heatmaps, pie charts)
- **PyPortfolioOpt** – Portfolio optimization and efficient frontier modeling
- **python-pptx** – Automated generation of PowerPoint presentation

---

**Project Features**

- Retrieves real-time adjusted stock data from Yahoo Finance
- Calculates daily returns, expected returns, and covariance
- Visualizes:
  - Price trends
  - Correlation heatmap
  - Efficient frontier
  - Optimized allocation pie chart
- Uses **Sharpe ratio maximization** to recommend a portfolio
- Converts allocation weights into **real-world discrete share purchases**
- Outputs results to a `.csv` file

---

**Results Summary for $20,000 Growth Portfolio**

- Portfolio optimized based on risk-return trade-off using mean-variance analysis
- Investment spread across high-performing tech and AI stocks with constraints to limit overexposure
- Model efficiently allocated $20,000 into whole shares, leaving < $10 unallocated
- Fully adaptable for different clients, sectors, or stock lists

