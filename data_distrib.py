import pandas as pd
import yfinance as yf
from matplotlib import pyplot as plt
import numpy as np

gain_sell = 10

#'ABNB'

ticker_symbols = ['ADBE', 'ABNB', 'AMD', 'GOOGL', 'GOOG', 'AMZN', 'AEP', 'AMGN', 'ADI', 'ANSS', 'AAPL', 'AMAT', 'ASML', 
'AZN', 'TEAM', 'ADSK', 'ADP', 'BKR', 'BIIB', 'BKNG', 'AVGO', 'CDNS', 'CDW', 'CHTR', 'CTAS', 'CSCO', 'CCEP', 'CTSH', 'CMCSA', 'CEG',
'CPRT', 'CSGP', 'COST', 'CRWD', 'CSX', 'DDOG', 'DXCM', 'FANG', 'DLTR', 'DASH', 'EA', 'EXC', 'FAST', 'FTNT', 'GILD', 'GFS',
'HON', 'IDXX', 'ILMN', 'INTC', 'INTU', 'ISRG', 'KDP', 'KLAC', 'KHC', 'LRCX', 'LIN', 'LULU', 'MAR', 'MRVL', 'MELI', 'META', 'MCHP',
'MU', 'MSFT', 'MRNA', 'MDLZ', 'MDB', 'MNST', 'NFLX', 'NVDA', 'NXPI', 'NDX', 'ORLY', 'ODFL', 'ON', 'PCAR', 'PANW', 'PAYX', 'PYPL', 'PDD',
'PEP', 'QCOM', 'REGN', 'ROP', 'ROST', 'SBUX', 'SMCI', 'SNPS', 'TTWO', 'TMUS', 'TSLA', 'TXN', 'TTD', 'VRSK', 'VRTX', 'WBD', 'WDAY',
'XEL', 'ZS']

stocks = {}

# Fetch historical data for each ticker
for symbol in ticker_symbols:
    try:
        ticker = yf.Ticker(symbol)
        historical_data = ticker.history(period='5y')
        if not historical_data.empty:
            stocks[symbol] = historical_data
    except Exception as e:
        print(f"Failed to fetch data for {symbol}: {e}")

# Create a new DataFrame to consolidate data
result_df = pd.DataFrame()

# Populate the DataFrame
for symbol in ticker_symbols:
    if symbol in stocks:
        stock_data = stocks[symbol][['Open']].rename(
            columns={
                'Open': f'{symbol}',
            }
        )
        if result_df.empty:
            result_df = stock_data
        else:
            result_df = result_df.join(stock_data)


print(result_df)
# Assuming 'results_df' is your dataframe
# Calculate percentage change for all stocks
pct_changes = (result_df.pct_change(periods=1))*100
# Flatten the dataframe into a single array
all_pct_changes = pct_changes[1:].values.flatten()
negative_returns = all_pct_changes[all_pct_changes <= -5]

# Plot the histogram
plt.figure(figsize=(14, 6))
plt.hist(negative_returns, bins=30, edgecolor='k', alpha=0.7)
plt.title('Histogram of Percentage Changes for All Stocks')
plt.xlabel('Percentage Change')
plt.ylabel('Frequency')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


max_val = np.max(negative_returns)
min_val = np.min(negative_returns)
mean_val = np.mean(negative_returns)
median_val = np.median(negative_returns)
std_dev = np.std(negative_returns)
q25 = np.percentile(negative_returns, 25)
q75 = np.percentile(negative_returns, 75)
n_obs = len(negative_returns)
below_5_percent = np.sum(all_pct_changes < -5)

# Print the results
print(f"Max: {max_val}")
print(f"Min: {min_val}")
print(f"Mean: {mean_val}")
print(f"Median: {median_val}")
print(f"Standard Deviation: {std_dev}")
print(f"25th Percentile: {q25}")
print(f"75th Percentile: {q75}")
print(f"Number of Observations: {n_obs}")
print(f"Number of Observations Below 5%: {below_5_percent}")

