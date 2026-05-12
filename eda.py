import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.ylabel('Frequency')
plt.show()

# Volume Analysis
plt.figure(figsize=(14, 6))
plt.plot(df['Volume'])
plt.title('Trading Volume')
plt.xlabel('Date')
plt.ylabel('Volume')
plt.grid(True)
plt.show()

# Candlestick Chart
fig = go.Figure(data=[go.Candlestick(
    x=df.index,
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close']
)])

fig.update_layout(
    title='Candlestick Chart',
    xaxis_title='Date',
    yaxis_title='Stock Price'
)

fig.show()

# Multiple Stock Correlation
stocks = ['AAPL', 'MSFT', 'TSLA', 'GOOGL']

multi_data = yf.download(stocks, start="2020-01-01")['Close']

returns = multi_data.pct_change()

correlation = returns.corr()

plt.figure(figsize=(10, 6))
sns.heatmap(correlation, annot=True)
plt.title('Stock Correlation Heatmap')
plt.show()

# Portfolio Comparison
portfolio_returns = returns.mean()
portfolio_risk = returns.std()

comparison = pd.DataFrame({
    'Returns': portfolio_returns,
    'Risk': portfolio_risk
})

print("\nPortfolio Comparison:")
print(comparison)

# Risk vs Return Plot
plt.figure(figsize=(10, 6))
plt.scatter(portfolio_risk, portfolio_returns)

for i in comparison.index:
    plt.text(portfolio_risk[i], portfolio_returns[i], i)

plt.xlabel('Risk')
plt.ylabel('Expected Return')
plt.title('Risk vs Return Analysis')
plt.grid(True)
plt.show()