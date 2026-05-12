import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Stock Market Analytics Dashboard", layout="wide")

st.title("📈 Stock Market Analytics Dashboard")

# Sidebar inputs
stock = st.sidebar.text_input("Enter Stock Symbol", "AAPL")

start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2025-01-01"))

# Download data
df = yf.download(stock, start=start_date, end=end_date)

# FIX 1: Flatten MultiIndex (IMPORTANT)
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# Safety check
if df.empty:
    st.error("No data found. Check stock symbol.")
    st.stop()

# Dataset
st.subheader("Dataset")
st.write(df.tail())

# Closing price
st.subheader("Closing Price Trend")
st.line_chart(df['Close'])

# FIX 2: Indicators MUST be created before plotting
df['MA50'] = df['Close'].rolling(window=50).mean()
df['MA200'] = df['Close'].rolling(window=200).mean()
df['Daily Return'] = df['Close'].pct_change()

# Moving averages (FIXED LINE)
st.subheader("Moving Averages")

chart_data = df[['Close', 'MA50', 'MA200']].dropna()
st.line_chart(chart_data)

# Daily returns
st.subheader("Daily Returns")
st.line_chart(df['Daily Return'])

# Volume
st.subheader("Volume")
st.bar_chart(df['Volume'])

# Candlestick chart
st.subheader("Candlestick Chart")

fig = go.Figure(data=[go.Candlestick(
    x=df.index,
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close']
)])

fig.update_layout(title=f"{stock} Candlestick Chart", xaxis_title="Date", yaxis_title="Price")

st.plotly_chart(fig, use_container_width=True)

# Risk metrics
st.subheader("Risk Analysis")

volatility = df['Daily Return'].std()
avg_return = df['Daily Return'].mean()

col1, col2 = st.columns(2)

col1.metric("Average Return", round(avg_return, 5))
col2.metric("Volatility", round(volatility, 5))