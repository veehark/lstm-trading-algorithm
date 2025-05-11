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

# Function to calculate rank-based allocation
def rank_based_allocation(df, return_cols):
    ranks = df[return_cols].rank(axis=1, ascending=False)  # Rank predicted returns (higher = better)
    num_stocks = ranks.shape[1]

    # Define allocation tiers
    top_weight = 0.6  # Top 20% get 50% allocation
    mid_weight = 0.4  # Middle 30% get 30% allocation
    low_weight = 0.0  # Bottom 50% get 20% allocation

    top_threshold = int(num_stocks * 0.2)
    mid_threshold = int(num_stocks * 0.5)

    allocations = np.zeros_like(ranks)

    for i in range(len(ranks)):
        sorted_indices = ranks.iloc[i].sort_values().index.to_list()  # Convert index to list

        allocations[i, [return_cols.index(col) for col in sorted_indices[:top_threshold]]] = top_weight / top_threshold
        allocations[i, [return_cols.index(col) for col in sorted_indices[top_threshold:mid_threshold]]] = mid_weight / (mid_threshold - top_threshold)
        allocations[i, [return_cols.index(col) for col in sorted_indices[mid_threshold:]]] = low_weight / (num_stocks - mid_threshold)

    return pd.DataFrame(allocations, columns=[col.replace('_Predicted_Return', '_allocation') for col in return_cols], index=df.index)


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

    
    allocations = rank_based_allocation(full_df, predicted_return_cols)

    full_df = pd.concat([full_df, allocations], axis=1)

    # Compute portfolio return: sum of (log return * allocation)
    log_return_cols = [col for col in full_df.columns if col.endswith('_log_return')]
    allocation_cols = [col.replace('_log_return', '_allocation') for col in log_return_cols]
    full_df['Portfolio_Return'] = (full_df[log_return_cols].values * full_df[allocation_cols].values).sum(axis=1)

    full_df.to_csv(returns_path + f"results_for_my_method_{folder}_rank.csv")

    for col in log_return_cols:
        stock_name = col.replace('_log_return', '')
        full_df[f'{stock_name}_cumulative_return'] = full_df[col].cumsum()

    full_df['Portfolio_Cumulative_Return'] = full_df['Portfolio_Return'].cumsum()

    individual_stocks_cumulative_returns = [f'{col.replace("_log_return", "_cumulative_return")}' for col in log_return_cols]
    full_df['Average_Cumulative_Return'] = full_df[individual_stocks_cumulative_returns].mean(axis=1)

    full_df.to_csv(returns_path + f"results_for_my_method_{folder}_cumulative_rank.csv", sep=';', decimal=',')

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
