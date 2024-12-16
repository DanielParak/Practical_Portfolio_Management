import yfinance as yf
import pandas as pd
import numpy as np
import openpyxl
from matplotlib import pyplot as plt

# Parameter Setting
bad_state_threshold = -5
observation_period = "5y"
plot_results = True
save_pic = True
save = False
lag_returns = [2,3,4,5,10,15,20,30]
time_windows = [1,2,3,4,5,10,15,20,30]

ticker = yf.Ticker("NDX")
Nasdaq_100 = ticker.history(period=observation_period)

Nasdaq_100['1d_lag'] = Nasdaq_100['Open'].shift()
Nasdaq_100 = Nasdaq_100[['Open','1d_lag']]

for lag in lag_returns:
    Nasdaq_100[f'{lag}d_lag'] = Nasdaq_100['Open'].shift(lag)

Nasdaq_100['1d_change'] = ((Nasdaq_100['Open'] - Nasdaq_100['1d_lag'])/Nasdaq_100['1d_lag']) * 100
for lag in lag_returns:
    Nasdaq_100[f'{lag}d_change'] = ((Nasdaq_100['Open'] - Nasdaq_100[f'{lag}d_lag'])/Nasdaq_100[f'{lag}d_lag']) * 100

Nasdaq_100['1d_bad_state'] = np.where(
    Nasdaq_100['1d_change']  <= bad_state_threshold,
    1,
    0
)
for lag in lag_returns:
    Nasdaq_100[f'{lag}d_bad_state'] = np.where(
    Nasdaq_100[f'{lag}d_change']  <= bad_state_threshold,
    1,
    0
)

# get forward look
Nasdaq_100['1d_forward'] = Nasdaq_100['Open'].shift(-1)
for lag in lag_returns:
    Nasdaq_100[f'{lag}d_forward'] =Nasdaq_100['Open'].shift(-lag)

Nasdaq_100['1d_forward_return'] = ((Nasdaq_100['1d_forward'] - Nasdaq_100['Open'])/Nasdaq_100['Open'])*100
for lag in lag_returns:
    Nasdaq_100[f'{lag}d_forward_return'] = ((Nasdaq_100[f'{lag}d_forward'] - Nasdaq_100['Open'])/Nasdaq_100['Open'])*100

# Nasdaq_100['1d_bad_state_1d_forward_return'] = Nasdaq_100['1d_forward_return'] * Nasdaq_100['1d_bad_state']

#over all bad state days
for lag_1 in time_windows:
    #over all forward_returns
    for lag_2 in time_windows:
        Nasdaq_100[f'{lag_1}d_bad_state_{lag_2}d_forward_return'] = Nasdaq_100[f'{lag_1}d_bad_state'] * Nasdaq_100[f'{lag_2}d_forward_return']

returns = [
    '1d_forward_return',
    '2d_forward_return',
    '3d_forward_return',
    '4d_forward_return',
    '5d_forward_return',
    '10d_forward_return',
    '15d_forward_return',
    '20d_forward_return',
    '30d_forward_return',
    "1d_bad_state_1d_forward_return",
    "1d_bad_state_2d_forward_return",
    "1d_bad_state_3d_forward_return",
    "1d_bad_state_4d_forward_return",
    "1d_bad_state_5d_forward_return",
    "1d_bad_state_10d_forward_return",
    "1d_bad_state_15d_forward_return",
    "1d_bad_state_20d_forward_return",
    "1d_bad_state_30d_forward_return",
    "2d_bad_state_1d_forward_return",
    "2d_bad_state_2d_forward_return",
    "2d_bad_state_3d_forward_return",
    "2d_bad_state_4d_forward_return",
    "2d_bad_state_5d_forward_return",
    "2d_bad_state_10d_forward_return",
    "2d_bad_state_15d_forward_return",
    "2d_bad_state_20d_forward_return",
    "2d_bad_state_30d_forward_return",
    "3d_bad_state_1d_forward_return",
    "3d_bad_state_2d_forward_return",
    "3d_bad_state_3d_forward_return",
    "3d_bad_state_4d_forward_return",
    "3d_bad_state_5d_forward_return",
    "3d_bad_state_10d_forward_return",
    "3d_bad_state_15d_forward_return",
    "3d_bad_state_20d_forward_return",
    "3d_bad_state_30d_forward_return",
    "4d_bad_state_1d_forward_return",
    "4d_bad_state_2d_forward_return",
    "4d_bad_state_3d_forward_return",
    "4d_bad_state_4d_forward_return",
    "4d_bad_state_5d_forward_return",
    "4d_bad_state_10d_forward_return",
    "4d_bad_state_15d_forward_return",
    "4d_bad_state_20d_forward_return",
    "4d_bad_state_30d_forward_return",
    "5d_bad_state_1d_forward_return",
    "5d_bad_state_2d_forward_return",
    "5d_bad_state_3d_forward_return",
    "5d_bad_state_4d_forward_return",
    "5d_bad_state_5d_forward_return",
    "5d_bad_state_10d_forward_return",
    "5d_bad_state_15d_forward_return",
    "5d_bad_state_20d_forward_return",
    "5d_bad_state_30d_forward_return",
    "10d_bad_state_1d_forward_return",
    "10d_bad_state_2d_forward_return",
    "10d_bad_state_3d_forward_return",
    "10d_bad_state_4d_forward_return",
    "10d_bad_state_5d_forward_return",
    "10d_bad_state_10d_forward_return",
    "10d_bad_state_15d_forward_return",
    "10d_bad_state_20d_forward_return",
    "10d_bad_state_30d_forward_return",
    "15d_bad_state_1d_forward_return",
    "15d_bad_state_2d_forward_return",
    "15d_bad_state_3d_forward_return",
    "15d_bad_state_4d_forward_return",
    "15d_bad_state_5d_forward_return",
    "15d_bad_state_10d_forward_return",
    "15d_bad_state_15d_forward_return",
    "15d_bad_state_20d_forward_return",
    "15d_bad_state_30d_forward_return",
    "20d_bad_state_1d_forward_return",
    "20d_bad_state_2d_forward_return",
    "20d_bad_state_3d_forward_return",
    "20d_bad_state_4d_forward_return",
    "20d_bad_state_5d_forward_return",
    "20d_bad_state_10d_forward_return",
    "20d_bad_state_15d_forward_return",
    "20d_bad_state_20d_forward_return",
    "20d_bad_state_30d_forward_return",
    "30d_bad_state_1d_forward_return",
    "30d_bad_state_2d_forward_return",
    "30d_bad_state_3d_forward_return",
    "30d_bad_state_4d_forward_return",
    "30d_bad_state_5d_forward_return",
    "30d_bad_state_10d_forward_return",
    "30d_bad_state_15d_forward_return",
    "30d_bad_state_20d_forward_return",
    "30d_bad_state_30d_forward_return"
]


results_df = pd.DataFrame(Nasdaq_100[returns])
Nasdaq_100 = Nasdaq_100[30:-30]
Nasdaq_100 = Nasdaq_100.reset_index()
results_df = results_df[1:-30]
results_df = results_df.reset_index()

non_zero_results = {column: Nasdaq_100.loc[Nasdaq_100[column] != 0, column] for column in returns}

description_df = Nasdaq_100[returns].describe()

all_non_zero_data = pd.concat(non_zero_results.values())
global_min = all_non_zero_data.min()
global_max = all_non_zero_data.max()

column_means = {column: data.mean() for column, data in non_zero_results.items()}

Nasdaq_100['average_market_1d_return'] = column_means['1d_forward_return']
Nasdaq_100['1d_return_above_market'] = Nasdaq_100['1d_forward_return'] - Nasdaq_100['average_market_1d_return']
Nasdaq_100['1d_return_above_market_one_hot'] = np.where(
    Nasdaq_100['1d_return_above_market'] > 0,
    1,
    0
)
print(Nasdaq_100[['1d_return_above_market_one_hot', '1d_return_above_market']])

alpha_dict = {}
for lag_1 in time_windows:
    for lag_2 in time_windows:
        alpha_dict[f'{lag_2}d_bad_state_{lag_1}d_forward_alpha'] = column_means[f'{lag_2}d_bad_state_{lag_1}d_forward_return'] - column_means[f'{lag_1}d_forward_return']

sorted_means = dict(sorted(column_means.items()))
sorted_alpha = dict(sorted(alpha_dict.items()))

if plot_results:
    plt.figure(figsize=(20, 8))  # Wide frame for better readability
    plt.bar(alpha_dict.keys(), alpha_dict.values(), color='coral', edgecolor='black')

    # Add titles and labels
    plt.title('Alpha Above Market Mean for Each Column', fontsize=16)
    plt.xlabel('Columns', fontsize=12)
    plt.ylabel('Alpha Value', fontsize=12)
    plt.xticks(rotation=90, ha='right', fontsize=10)  # Rotate column names for better visibility

    # Display the plot
    plt.tight_layout()  # Adjust layout for better fit
    plt.show()

    # Plot the bar chart
    plt.figure(figsize=(20, 8))  # Wide frame for better readability
    plt.bar(column_means.keys(), column_means.values(), color='skyblue', edgecolor='black')

    # Add titles and labels
    plt.title('Mean of Non-Zero Values for Each Column', fontsize=16)
    plt.xlabel('Columns', fontsize=12)
    plt.ylabel('Mean Value', fontsize=12)
    plt.xticks(rotation=90, ha='right', fontsize=10)  # Rotate column names for better visibility

    # Display the plot
    plt.tight_layout()  # Adjust layout for better fit
    plt.show()

    if save_pic:

        for column, non_zero_data in non_zero_results.items():
            # Calculate descriptive statistics
            desc = non_zero_results[column].describe()
            plt.figure(figsize=(14, 6))
            plt.hist(non_zero_data, bins=30, color='skyblue', edgecolor='black')
            plt.title(f'Histogram of Non-Zero Values: {column}')
            plt.xlabel('Returns')
            plt.ylabel('Frequency')
            plt.xlim(global_min, global_max)

            # Add the table with the descriptive statistics
            # Convert the description to a format usable by plt.table
            stats = desc.reset_index()  # Convert Series to DataFrame
            table_data = stats.values.tolist()  # Convert to list for table

            # Create the table
            table = plt.table(
                cellText=table_data,
                colLabels=['Statistic', 'Value'],
                loc='center right',  # Place it closer to the center
                cellLoc='center',
                bbox=[1.1, 0.1, 0.6, 0.8]  # Adjust the position and size of the table
            )

            # Adjust the layout to make space for the table
            plt.subplots_adjust(right=0.6)  # Allocate more space on the right
            plt.savefig(f'Pics/Nasdaq/{column}')
            plt.close()
            # Display the plot
            # plt.show()

if save:
    description_df.to_excel("Description_Nasdaq_returns.xlsx")