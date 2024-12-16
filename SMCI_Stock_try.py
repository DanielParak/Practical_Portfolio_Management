import pandas as pd
import yfinance as yf
from matplotlib import pyplot as plt


ticker_symbols = ['ADBE', 'AMD', 'ABNB', 'GOOGL', 'GOOG', 'AMZN', 'AEP', 'AMGN', 'ADI', 'ANSS', 'AAPL', 'AMAT', 'ARM', 'ASML', 
'AZN', 'TEAM', 'ADSK', 'ADP', 'BKR', 'BIIB', 'BKNG', 'AVGO', 'CDNS', 'CDW', 'CHTR', 'CTAS', 'CSCO', 'CCEP', 'CTSH', 'CMCSA', 'CEG',
'CPRT', 'CSGP', 'COST', 'CRWD', 'CSX', 'DDOG', 'DXCM', 'FANG', 'DLTR', 'DASH', 'EA', 'EXC', 'FAST', 'FTNT', 'GEHC', 'GILD', 'GFS',
'HON', 'IDXX', 'ILMN', 'INTC', 'INTU', 'ISRG', 'KDP', 'KLAC', 'KHC', 'LRCX', 'LIN', 'LULU', 'MAR', 'MRVL', 'MELI', 'META', 'MCHP',
'MU', 'MSFT', 'MRNA', 'MDLZ', 'MDB', 'MNST', 'NFLX', 'NVDA', 'NXPI', 'ORLY', 'ODFL', 'ON', 'PCAR', 'PANW', 'PAYX', 'PYPL', 'PDD',
'PEP', 'QCOM', 'REGN', 'ROP', 'ROST', 'SBUX', 'SMCI', 'SNPS', 'TTWO', 'TMUS', 'TSLA', 'TXN', 'TTD', 'VRSK', 'VRTX', 'WBD', 'WDAY',
'XEL', 'ZS']


# Dictionary to store historical data
stocks = {}

# Fetch historical data for each ticker
for symbol in ticker_symbols:
    try:
        ticker = yf.Ticker(symbol)
        historical_data = ticker.history(period="1y")
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


result_df['SMCI_1d_lag'] = result_df['SMCI'].shift()
result_df['SMCI_stock_change'] = ((result_df['SMCI']-result_df['SMCI_1d_lag'])/result_df['SMCI_1d_lag'])*100
print(result_df)

result_df['bad_state'] = (result_df['SMCI_stock_change'] <= -10).astype(int)

bad_state_rows = result_df[result_df['bad_state'] == 1]


bad_state_indices = result_df[result_df['bad_state'] == 1].index

mean_change = []
for idx in bad_state_indices:
    start_index = result_df.index.get_loc(idx)  # Get the position of the row
    start_price = result_df.iloc[start_index]['SMCI']
    try:
        end_price = result_df.iloc[start_index + 5]['SMCI']
    except IndexError:
        end_price =start_price
    percentage_change = ((end_price-start_price)/start_price) * 100
    print(start_price)
    print(end_price)
    print("Our AWESOME STRATEGY RETURNS: ",percentage_change,"%" )
    mean_change.append(percentage_change)
    print(result_df.iloc[start_index:start_index + 6])  # Print 6 rows starting from the bad state row
    print("\n" + "-" * 40 + "\n") 

print("FINAL RESULT :",sum(mean_change)/len(mean_change),"%")


# plt.plot(result_df['SMCI'])
# plt.show()


