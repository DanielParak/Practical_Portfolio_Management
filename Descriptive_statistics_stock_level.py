import pandas as pd
import yfinance as yf
from matplotlib import pyplot as plt
import numpy as np

# Parameter Setting
lookforward = -29
name_lookforward = (lookforward*(-1))+1
bad_state_threshold = -10
observation_period = "5y"
plot_results = True

ticker_symbols = ['ADBE', 'AMD', 'ABNB', 'GOOGL', 'GOOG', 'AMZN', 'AEP', 'AMGN', 'ADI', 'ANSS', 'AAPL', 'AMAT', 'ASML', 
'AZN', 'TEAM', 'ADSK', 'ADP', 'BKR', 'BIIB', 'BKNG', 'AVGO', 'CDNS', 'CDW', 'CHTR', 'CTAS', 'CSCO', 'CCEP', 'CTSH', 'CMCSA', 'CEG',
'CPRT', 'CSGP', 'COST', 'CRWD', 'CSX', 'DDOG', 'DXCM', 'FANG', 'DLTR', 'DASH', 'EA', 'EXC', 'FAST', 'FTNT', 'GILD', 'GFS',
'HON', 'IDXX', 'ILMN', 'INTC', 'INTU', 'ISRG', 'KDP', 'KLAC', 'KHC', 'LRCX', 'LIN', 'LULU', 'MAR', 'MRVL', 'MELI', 'META', 'MCHP',
'MU', 'MSFT', 'MRNA', 'MDLZ', 'MDB', 'MNST', 'NFLX', 'NVDA', 'NXPI', 'ORLY', 'ODFL', 'ON', 'PCAR', 'PANW', 'PAYX', 'PYPL', 'PDD',
'PEP', 'QCOM', 'REGN', 'ROP', 'ROST', 'SBUX', 'SMCI', 'SNPS', 'TTWO', 'TMUS', 'TSLA', 'TXN', 'TTD', 'VRSK', 'VRTX', 'WBD', 'WDAY',
'XEL', 'ZS']

# for 5 years exclude 'ARM', 'GEHC'

# Dictionary to store historical data
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


dataframes = []

# Iterate over the ticker symbols
for symbol in ticker_symbols:
    if symbol in result_df.columns:
        # Create a new DataFrame for this symbol
        temp_df = result_df[[symbol]].copy()  # Work with the relevant column
        
        # Perform the calculations
        temp_df[f'{symbol}_1d_lag'] = temp_df[symbol].shift()
        temp_df[f'{symbol}_{name_lookforward}d_forward'] = temp_df[symbol].shift(periods=lookforward)
        temp_df[f'{symbol}_stock_change'] = ((temp_df[symbol] - temp_df[f'{symbol}_1d_lag']) / temp_df[f'{symbol}_1d_lag']) * 100
        temp_df[f'{symbol}_bad_state'] = (temp_df[f'{symbol}_stock_change'] <= bad_state_threshold).astype(int)
        temp_df[f'{symbol}_bad_state_{name_lookforward}d_forward'] = temp_df[f'{symbol}_bad_state'] * temp_df[f'{symbol}_{name_lookforward}d_forward']
        temp_df[f'{symbol}_bad_state_{name_lookforward}d_forward_change'] = np.where(
        temp_df[f'{symbol}_bad_state'] == 1,
        ((temp_df[f'{symbol}_bad_state_{name_lookforward}d_forward'] - temp_df[symbol]) / temp_df[symbol]) * 100,
        0
        )
   
        dataframes.append(temp_df)
final_df = pd.concat(dataframes, axis=1)

final_df['market_cap'] = final_df[ticker_symbols].sum(axis=1)
final_df['market_cap_1d_lag'] = final_df['market_cap'].shift()
final_df['market_change'] = ((final_df['market_cap'] - final_df['market_cap_1d_lag'])/final_df['market_cap_1d_lag'])*100
final_df[f'market_{name_lookforward}d_forward'] = final_df['market_cap'].shift(periods=lookforward)
final_df[f'market_{name_lookforward}d_forward_change_m'] = ((final_df[f'market_{name_lookforward}d_forward'] - final_df['market_cap']) /  final_df['market_cap'])*100

bad_states_col_name = []
for col in final_df:
    if col.endswith("bad_state"):
        bad_states_col_name.append(col)
bad_states_gain_col = []
for col in final_df:
    if col.endswith("forward_change"):
        bad_states_gain_col.append(col)
# Next steps: Find the average of the bad_state_5d_forward performance and benchmark it against the average 5d forward market performance
# final_df['bad_states_count'] = (final_df[bad_states_col_name] == 1).sum()
final_df['bad_states_count'] = final_df[bad_states_col_name].sum(axis=1)
final_df['bad_state_gain_sum'] = final_df[bad_states_gain_col].sum(axis=1)
final_df[f'bad_state_gain_avg_{name_lookforward}d'] = final_df['bad_state_gain_sum'] / final_df['bad_states_count']

final_df['gain_above_market'] = final_df[f'bad_state_gain_avg_{name_lookforward}d'] - final_df[f'market_{name_lookforward}d_forward_change_m']

final_df = final_df.reset_index()

if plot_results:

    plt.hist(final_df[['gain_above_market']][1:], bins=30, color='skyblue', edgecolor='black')
    plt.title("Gain Above Market Histogram")
    plt.xlabel("Values")
    plt.ylabel("Frequency")
    plt.show()

    print(final_df[[f'bad_state_gain_avg_{name_lookforward}d']][1:].describe())
    print(final_df[[f'market_{name_lookforward}d_forward_change_m']][1:].describe())
    print(final_df[['gain_above_market']][1:].describe())


    plt.hist(final_df[[f'bad_state_gain_avg_{name_lookforward}d']][1:], bins=30, color='skyblue', edgecolor='black')
    # Adding labels and title
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title('Histogram Bad State Gain')
    # Display the plot
    plt.show()

    plt.hist(final_df[[f'market_{name_lookforward}d_forward_change_m']][1:], bins=30, color='skyblue', edgecolor='black')
    # Adding labels and title
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title('Histogram Market Gain')
    # Display the plot
    plt.show()

    plt.plot(final_df['market_cap']/final_df['market_cap'][0])
    plt.title(f'Nasdaq-100 relative development {observation_period}')
    plt.show()

