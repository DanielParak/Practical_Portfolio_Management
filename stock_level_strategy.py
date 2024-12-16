import pandas as pd
import yfinance as yf
from matplotlib import pyplot as plt
import numpy as np

gain_sell = 20
gain_sells = [5,10,15,20,30,50,100]
return_threshold = -0.04
return_thresholds = [0, -0.02, -0.04, -0.05, -0.07, -0.1]
observation_period = "5y"
investment_amount = 0.1
initial_cash = 10000000

ticker_symbols = ['ADBE', 'AMD', 'ABNB', 'GOOGL', 'GOOG', 'AMZN', 'AEP', 'AMGN', 'ADI', 'ANSS', 'AAPL', 'AMAT', 'ASML', 
'AZN', 'TEAM', 'ADSK', 'ADP', 'BKR', 'BIIB', 'BKNG', 'AVGO', 'CDNS', 'CDW', 'CHTR', 'CTAS', 'CSCO', 'CCEP', 'CTSH', 'CMCSA', 'CEG',
'CPRT', 'CSGP', 'COST', 'CRWD', 'CSX', 'DDOG', 'DXCM', 'FANG', 'DLTR', 'DASH', 'EA', 'EXC', 'FAST', 'FTNT', 'GILD', 'GFS',
'HON', 'IDXX', 'ILMN', 'INTC', 'INTU', 'ISRG', 'KDP', 'KLAC', 'KHC', 'LRCX', 'LIN', 'LULU', 'MAR', 'MRVL', 'MELI', 'META', 'MCHP',
'MU', 'MSFT', 'MRNA', 'MDLZ', 'MDB', 'MNST', 'NFLX', 'NVDA', 'NXPI', 'ORLY', 'ODFL', 'ON', 'PCAR', 'PANW', 'PAYX', 'PYPL', 'PDD',
'PEP', 'QCOM', 'REGN', 'ROP', 'ROST', 'SBUX', 'SMCI', 'SNPS', 'TTWO', 'TMUS', 'TSLA', 'TXN', 'TTD', 'VRSK', 'VRTX', 'WBD', 'WDAY',
'XEL', 'ZS']

DAX_symbols = ['ADS', 'AIR', 'ALV', 'BAS', 'BAYN', 'BEI', 'BMW', 'BNR', 'CBK', 'CON', '1COV', 'DTG',
               'DBK', 'DB1', 'DHL', 'DTE', 'EOAN', 'FRE', 'HNR1', 'HEI', 'HEN3', 'IFX', 'MBG', 'MRK',
                'MTX', 'MUV2', 'P911', 'PAH3', 'QIA', 'RHM', 'RWE', 'SAP', 'SRT3', 'SIE', 'ENR', 'SHL',
                'SY1', 'VOW3', 'VNA', 'ZAL']

SP500_symbols = ['MMM', 'AOS', 'ABT', 'ABBV', 'ACN', 'ADBE', 'AMD', 'AES', 'AFL', 'A', 'APD', 'ABNB',
                    'AKAM', 'ALB', 'ARE', 'ALGN', 'ALLE', 'LNT', 'ALL', 'GOOGL', 'GOOG', 'MO', 'AMZN',
                     'AMCR', 'AMTM', 'AEE', 'AEP', 'AXP', 'AIG', 'AMT', 'AWK', 'AMP', 'AME', 'AMGN', 
                     'APH', 'ADI', 'ANSS', 'AON', 'APA', 'AAPL', 'AMAT', 'APTV', 'ACGL', 'ADM', 'ANET'
                     , 'AJG', 'AIZ', 'T', 'ATO', 'ADSK', 'ADP', 'AZO', 'AVB', 'AVY', 'AXON', 'BKR',
                     'BALL', 'BAC', 'BAX', 'BDX', 'BRK.B', 'BBY', 'TECH', 'BIIB', 'BLK', 'BX', 'BK',
                     'BA', 'BKNG', 'BWA', 'BSX', 'BMY', 'AVGO', 'BR', 'BRO', 'BF.B', 'BLDR', 'BG', 
                     'BXP', 'CHRW', 'CDNS', 'CZR', 'CPT', 'CPB', 'COF', 'CAH', 'KMX', 'CCL', 'CARR'
                     ,'CTLT', 'CAT', 'CBOE', 'CBRE', 'CDW', 'CE', 'COR', 'CNC', 'CNP', 'CF', 'CRL'
                     ,'SCHW', 'CHTR', 'CVX', 'CMG', 'CB', 'CHD', 'CI', 'CINF', 'CTAS', 'CSCO', 'C'
                     ,'CFG', 'CLX', 'CME', 'CMS', 'KO', 'CTSH', 'CL', 'CMCSA', 'CAG', 'COP',
                     'ED', 'STZ', 'CEG', 'COO', 'CPRT', 'GLW', 'CPAY', 'CTVA', 'CSGP', 'COST',
                     'CTRA', 'CRWD', 'CCI', 'CSX', 'CMI', 'CVS', 'DHR', 'DRI', 'DVA', 'DAY',
                     'DECK', 'DE', 'DELL', 'DAL', 'DVN', 'DXCM', 'FANG', 'DLR', 'DFS', 'DG',
                     'DLTR', 'D', 'DPZ', 'DOV', 'DOW', 'DHI', 'DTE', 'DUK', 'DD', 'EMN',
                     'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'ELV', 'EMR', 'ENPH', 'ETR', 'EOG', 'EPAM', 'EQT', 'EFX', 'EQIX', 'EQR', 'ERIE', 'ESS', 'EL', 'EG', 'EVRG', 'ES', 'EXC', 'EXPE', 'EXPD', 'EXR', 'XOM', 'FFIV', 'FDS', 'FICO', 'FAST', 'FRT', 'FDX', 'FIS', 'FITB', 'FSLR', 'FE', 'FI', 'FMC', 'F', 'FTNT', 'FTV', 'FOXA', 'FOX', 'BEN', 'FCX', 'GRMN', 'IT', 'GE', 'GEHC', 'GEV', 'GEN', 'GNRC', 'GD', 'GIS', 'GM', 'GPC', 'GILD', 'GPN', 'GL', 'GDDY', 'GS', 'HAL', 'HIG', 'HAS', 'HCA', 'DOC', 'HSIC', 'HSY', 'HES', 'HPE', 'HLT', 'HOLX', 'HD', 'HON', 'HRL', 'HST', 'HWM', 'HPQ', 'HUBB', 'HUM', 'HBAN', 'HII', 'IBM', 'IEX', 'IDXX', 'ITW', 'INCY', 'IR', 'PODD', 'INTC', 'ICE', 'IFF', 'IP', 'IPG', 'INTU', 'ISRG', 'IVZ', 'INVH', 'IQV', 'IRM', 'JBHT', 'JBL', 'JKHY', 'J', 'JNJ', 'JCI', 'JPM', 'JNPR', 'K', 'KVUE', 'KDP', 'KEY', 'KEYS', 'KMB', 'KIM', 'KMI', 'KKR', 'KLAC', 'KHC', 'KR', 'LHX', 'LH', 'LRCX', 'LW', 'LVS', 'LDOS', 'LEN', 'LLY', 'LIN', 'LYV', 'LKQ', 'LMT', 'L', 'LOW', 'LULU', 'LYB', 'MTB', 'MPC', 'MKTX', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MTCH', 'MKC', 'MCD', 'MCK', 'MDT', 'MRK', 'META', 'MET', 'MTD', 'MGM', 'MCHP', 'MU', 'MSFT', 'MAA', 'MRNA', 'MHK', 'MOH', 'TAP', 'MDLZ', 'MPWR', 'MNST', 'MCO', 'MS', 'MOS', 'MSI', 'MSCI', 'NDAQ', 'NTAP', 'NFLX', 'NEM', 'NWSA', 'NWS', 'NEE', 'NKE', 'NI', 'NDSN', 'NSC', 'NTRS', 'NOC', 'NCLH', 'NRG', 'NUE', 'NVDA', 'NVR', 'NXPI', 'ORLY', 'OXY', 'ODFL', 'OMC', 'ON', 'OKE', 'ORCL', 'OTIS', 'PCAR', 'PKG', 'PLTR', 'PANW', 'PARA', 'PH', 'PAYX', 'PAYC', 'PYPL', 'PNR', 'PEP', 'PFE', 'PCG', 'PM', 'PSX', 'PNW', 'PNC', 'POOL', 'PPG', 'PPL', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PTC', 'PSA', 'PHM', 'QRVO', 'PWR', 'QCOM', 'DGX', 'RL', 'RJF', 'RTX', 'O', 'REG', 'REGN', 'RF', 'RSG', 'RMD', 'RVTY', 'ROK', 'ROL', 'ROP', 'ROST', 'RCL', 'SPGI', 'CRM', 'SBAC', 'SLB', 'STX', 'SRE', 'NOW', 'SHW', 'SPG', 'SWKS', 'SJM', 'SW', 'SNA', 'SOLV', 'SO', 'LUV', 'SWK', 'SBUX', 'STT', 'STLD', 'STE', 'SYK', 'SMCI', 'SYF', 'SNPS', 'SYY', 'TMUS', 'TROW', 'TTWO', 'TPR', 'TRGP', 'TGT', 'TEL', 'TDY', 'TFX', 'TER', 'TSLA', 'TXN', 'TPL', 'TXT', 'TMO', 'TJX', 'TSCO', 'TT', 'TDG', 'TRV', 'TRMB', 'TFC', 'TYL', 'TSN', 'USB', 'UBER', 'UDR', 'ULTA', 'UNP', 'UAL', 'UPS', 'URI', 'UNH', 'UHS', 'VLO', 'VTR', 'VLTO', 'VRSN', 'VRSK', 'VZ', 'VRTX', 'VTRS', 'VICI', 'V', 'VST', 'VMC', 'WRB', 'GWW', 'WAB', 'WBA', 'WMT', 'DIS', 'WBD', 'WM', 'WAT', 'WEC', 'WFC', 'WELL', 'WST', 'WDC', 'WY', 'WMB', 'WTW', 'WYNN', 'XEL', 'XYL', 'YUM', 'ZBRA', 'ZBH', 'ZTS']

Nasdaq_100 = yf.Ticker("NDX").history(period=observation_period)
df = Nasdaq_100[['Open']]
df['daily_return'] = df['Open'].pct_change()

stocks = {}

# Fetch historical data for each ticker
for symbol in ticker_symbols:
    try:
        ticker = yf.Ticker(symbol)
        historical_data = ticker.history(period=observation_period)
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

result_df.index = pd.to_datetime(result_df.index)

# Define the cutoff date
cutoff_date = pd.Timestamp('2020-02-10').tz_localize('America/New_York')

# Filter the dataframe
result_df = result_df[result_df.index > cutoff_date]


plot_whole = {}

for symbol in ticker_symbols:
    if symbol in stocks:
        result_df[f'{symbol}_daily_return'] = result_df[symbol].pct_change()
        result_df[f'{symbol}_buy_signal'] = result_df[f'{symbol}_daily_return'] < return_threshold

# Initial cash for both strategies
cash = initial_cash
holdings = 0
portfolio_value_dip = []  # Tracks portfolio value over time
portfolio_value_hold = []  # Tracks buy-and-hold strategy
cash_portfolio_value_dip = []
cash_quote_portfolio = []
investments = [] 
holding_len = []
holding = 0
holding_days = 0
buy_counter = 0
sell_counter = 0

nasdaq_cumulative_return = (1 + df['daily_return']).cumprod()
portfolio_value_hold = initial_cash * nasdaq_cumulative_return

for i, row in result_df.iterrows():
    for symbol in stocks:
        # Buy signal
        if row[f'{symbol}_buy_signal'] and cash > 0:
            buy_counter += 1
            buy_amount = cash * investment_amount  # Use 25% of cash for each dip
            shares_bought = buy_amount / row[symbol]
            holdings += shares_bought
            cash -= buy_amount

            # Record the purchase in the investments tracker
            investments.append({
                'date': i,  # Track purchase date
                'share': symbol,
                'shares': shares_bought,
                'price': row[symbol],  # Purchase price
                'days_held': 0,  # Initialize holding period
                'gain':0
            })

        for lot in investments:
            if lot['share'] == symbol:
                lot['days_held'] += 1  # Increment days held
                lot['gain'] = ((row[symbol] - lot['price'])/ lot['price']) * 100
        
        for lot in investments[:]:
            if lot['share'] == symbol and lot['gain'] >= gain_sell:
                sell_counter += 1
                sell_amount = lot['shares'] * row[symbol]  # Value of shares sold
                cash += sell_amount
                holdings -= lot['shares']
                investments.remove(lot)   # Remove the lot after selling

    portfolio_value = cash + sum(
        lot['shares'] * row[lot['share']] for lot in investments
    )
    cash_quote = (cash / portfolio_value) * 100

    cash_portfolio_value_dip.append(cash)
    portfolio_value_dip.append(portfolio_value)  
    cash_quote_portfolio.append(cash_quote)
    holding_len.append(holdings)     

result_df['portfolio_value_dip'] = portfolio_value_dip
result_df['cash'] = cash_portfolio_value_dip
result_df['portfolio_value_hold'] = portfolio_value_hold
result_df['portfolio_value_hold_pct'] = result_df['portfolio_value_hold'].pct_change()*100
result_df['cash_quote'] = cash_quote_portfolio
result_df['portfolio_value_dip_pct'] = result_df['portfolio_value_dip'].pct_change()*100
result_df['investment_len'] = holding_len

risk_free_rate = 0.03/365

# Calculate mean return and standard deviation from percentage changes
mean_return = result_df['portfolio_value_dip_pct'].mean()
std_dev = result_df['portfolio_value_dip_pct'].std()

# Sharpe Ratio calculation
sharpe_ratio = (mean_return - risk_free_rate) / std_dev

# Print the result
print(f"Sharpe Ratio: {sharpe_ratio}")
annualized_sharpe_ratio = sharpe_ratio * np.sqrt(252)
print("Annualized Sharpe Ratio:", annualized_sharpe_ratio)

fig, ax1 = plt.subplots(figsize=(20, 6))
# Plot the main data on the y-axis
ax1.plot(result_df['portfolio_value_dip'], label='Buy the Dip', color='blue')
ax1.plot(result_df['portfolio_value_hold'], label='Buy and Hold', color='green')
ax1.plot(result_df['cash'], label="Cash", color='orange')
ax1.set_xlabel("Time")
ax1.set_ylabel("Price", color='black')

ax2 = ax1.twinx()
ax2.plot(result_df.index, result_df['investment_len'], alpha=0.3, color='grey', label='Portfolio size')
ax2.set_ylabel("Portfolio size", color='grey')

# Combine legends from both axes
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

# Show the plot
plt.show()



print(result_df['portfolio_value_dip'].describe())
print("----------"*20)
print(result_df['portfolio_value_hold'].describe())
print("----------"*20)
print(result_df['portfolio_value_dip'].iloc[-1])
print("----------"*20)
print(result_df['portfolio_value_hold'].iloc[-2])
print("----------"*20)
print(result_df['portfolio_value_dip'].iloc[-1]/initial_cash)
print("----------"*20)
print(result_df['portfolio_value_hold'].iloc[-2]/initial_cash)
print("----------"*20)
print("Sell counter: ",sell_counter)
print("Buy Counter: ",buy_counter)
print("----------"*20)
print(result_df['investment_len'].describe())
print("----------"*20)
print(result_df['cash'].describe())
print("----------"*20)

# plot_whole[return_threshold] = portfolio_value_dip

# fig, ax = plt.subplots()

# # Iterate through the dictionary and plot each strategy
# for strategy, values in plot_whole.items():
#     ax.plot(values, label=strategy)

# # Add labels and title
# ax.set_xlabel("Time")
# ax.set_ylabel("Portfolio Value")
# ax.set_title("Portfolio Performance for Different Strategies")

# # Add the legend
# ax.legend(loc='upper left')

# # Show the plot
# plt.show()

portfolio_returns = result_df['portfolio_value_dip_pct'] / 100
market_returns = result_df['portfolio_value_hold_pct'] / 100
annual_risk_free_rate = 0.02
daily_risk_free_rate = annual_risk_free_rate / 252

# Portfolio's and market's average daily return
mean_portfolio_return = portfolio_returns.mean()
mean_market_return = market_returns.mean()

# Calculate beta
covariance = np.cov(portfolio_returns, market_returns)[0, 1]
market_variance = market_returns.var()
beta = covariance / market_variance

# Calculate alpha
alpha = mean_portfolio_return - (daily_risk_free_rate + beta * (mean_market_return - daily_risk_free_rate))

print("Beta:", beta)
print("Alpha:", alpha)