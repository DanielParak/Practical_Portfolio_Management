import requests
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd

Nasdaq_100 = yf.Ticker("^GSPC").history(period="5y")
print(Nasdaq_100)
df = Nasdaq_100[['Open']]
df['daily_return'] = df['Open'].pct_change()
print(df)

nasdaq_cumulative_return = (1 + df['daily_return']).cumprod()
stock_invest = 10000000/df['Open'][0]
portfolio_value_hold = df['Open']*stock_invest
print(portfolio_value_hold)