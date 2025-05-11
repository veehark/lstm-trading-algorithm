import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

folders = ['omxh', 'nse', 'nyse']
signals_path = 'C:/Users/vjtha/OneDrive - O365 Turun yliopisto/Pro gradu/results/signals/'
returns_path = 'C:/Users/vjtha/OneDrive - O365 Turun yliopisto/Pro gradu/results/allocation_return_results/'

def data_preparation(df):
    df = df.dropna(subset=['Model_Predicted_Prices'])  # Remove rows where prediction is missing
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df

import numpy as np
import pandas as pd

def exponential_allocation(df, return_cols, base=1):
    """
    Allocates weights exponentially based on predicted returns.
    
    Args:
        df (pd.DataFrame): DataFrame containing predicted returns.
        return_cols (list): List of column names for predicted returns.
        base (float): The base of the exponent (default=2). Higher values give more weight to top-ranked stocks.

    Returns:
        pd.DataFrame: DataFrame with allocation weights.
    """
    ranks = df[return_cols].rank(axis=1, ascending=False)  # Rank predicted returns (higher = better)
    num_stocks = len(return_cols)

    # Compute exponential weights
    exp_weights = base ** (num_stocks - ranks)  # Higher rank → higher weight
    exp_weights = exp_weights.div(exp_weights.sum(axis=1), axis=0)  # Normalize so row sums to 1

    # Rename columns to indicate allocation
    exp_allocations = exp_weights.rename(columns={col: col.replace('_Predicted_Return', '_allocation') for col in return_cols})

    return exp_allocations


for folder in folders:
    full_path = signals_path + folder + '/'
    full_results_path = returns_path + folder + '/'
    files = [f for f in os.listdir(full_path) if f.endswith('_signals.csv')]
    full_df = pd.DataFrame()

    for file in files:
        file_path = os.path.join(full_path, file)
        df = pd.read_csv(file_path)
        stock = file.split('_')[0]
        df = data_preparation(df)

        df_important = pd.DataFrame()
        close = stock + '_Close'
        log_return = stock + '_log_return'
        pred_price = stock + '_Model_Predicted_Prices'
        pred_return = stock + '_Predicted_Return'

        df_important[[close, pred_price]] = df[['Close', 'Model_Predicted_Prices']]
        df_important[pred_return] = df_important[pred_price] / df_important[close].shift(1) - 1
        df_important[log_return] = df_important[close] / df_important[close].shift(1) - 1

        full_df = pd.concat([full_df, df_important], axis=1)

    full_df = full_df.dropna()

    predicted_return_cols = [col for col in full_df.columns if col.endswith('_Predicted_Return')]
    if not predicted_return_cols:
        raise ValueError("No predicted return columns found!")

    
    allocations = exponential_allocation(full_df, predicted_return_cols, base=2)

    full_df = pd.concat([full_df, allocations], axis=1)

    # Compute portfolio return: sum of (log return * allocation)
    log_return_cols = [col for col in full_df.columns if col.endswith('_log_return')]
    allocation_cols = [col.replace('_log_return', '_allocation') for col in log_return_cols]
    full_df['Portfolio_Return'] = (full_df[log_return_cols].values * full_df[allocation_cols].values).sum(axis=1)

    full_df.to_csv(returns_path + f"results_for_my_method_{folder}_exp.csv")

    for col in log_return_cols:
        stock_name = col.replace('_log_return', '')
        full_df[f'{stock_name}_cumulative_return'] = full_df[col].cumsum()

    full_df['Portfolio_Cumulative_Return'] = full_df['Portfolio_Return'].cumsum()

    individual_stocks_cumulative_returns = [f'{col.replace("_log_return", "_cumulative_return")}' for col in log_return_cols]
    full_df['Average_Cumulative_Return'] = full_df[individual_stocks_cumulative_returns].mean(axis=1)

    full_df.to_csv(returns_path + f"results_for_my_method_{folder}_cumulative_exp.csv", sep=';', decimal=',')

    # Plot cumulative returns
    plt.figure(figsize=(10, 6))
    plt.plot(full_df.index, full_df['Portfolio_Cumulative_Return'], label='Portfolio', linewidth=2, color='black')

    for col in log_return_cols:
        stock_name = col.replace('_log_return', '')
        plt.plot(full_df.index, full_df[f'{stock_name}_cumulative_return'], linestyle='-', color='blue', alpha=0.3)

    plt.plot(full_df.index, full_df['Average_Cumulative_Return'], label='Average of Individual Stocks', linestyle='-', color='red', linewidth=2)

    plt.title(f"Cumulative Returns of Portfolio vs Individual Stocks (with Average), {folder}")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
