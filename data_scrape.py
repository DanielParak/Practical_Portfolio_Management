import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Function to fetch Nasdaq-100 tickers
def get_nasdaq_100_tickers():
    url = "https://en.wikipedia.org/wiki/NASDAQ-100"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "constituents"})
    tickers = [row.find_all("td")[1].text.strip() for row in table.find_all("tr")[1:]]
    return tickers

def get_dax_tickers():
    url = "https://en.wikipedia.org/wiki/DAX"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "wikitable sortable"})
    tickers = [row.find_all("td")[1].text.strip() for row in table.find_all("tr")[2:]]
    return tickers

DAX_tickers = get_dax_tickers()
print(DAX_tickers)
# Get Nasdaq-100 tickers
# ticker_symbols = get_nasdaq_100_tickers()
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
        historical_data = ticker.history(period="1y", interval="1h")
        if not historical_data.empty:
            stocks[symbol] = historical_data
    except Exception as e:
        print(f"Failed to fetch data for {symbol}: {e}")

# Create a new DataFrame to consolidate data
result_df = pd.DataFrame()

# Populate the DataFrame
for symbol in ticker_symbols:
    if symbol in stocks:
        stock_data = stocks[symbol][['Open', 'Close']].rename(
            columns={
                'Open': f'{symbol}_stock_open',
                'Close': f'{symbol}_stock_close'
            }
        )
        # Calculate percentage change
        stock_data[f'{symbol}_stock_change'] = (
            (stock_data[f'{symbol}_stock_close'] - stock_data[f'{symbol}_stock_open']) /
            stock_data[f'{symbol}_stock_open']
        ) * 100
        # Combine into a single DataFrame
        if result_df.empty:
            result_df = stock_data
        else:
            result_df = result_df.join(stock_data)


