import pandas as pd
import os
import numpy as np

folders = ['omxh', 'nse', 'nyse']
signals_path = 'C:/Users/vjtha/OneDrive - O365 Turun yliopisto/Pro gradu/results/signals/'
returns_path = 'C:/Users/vjtha/OneDrive - O365 Turun yliopisto/Pro gradu/results/allocation_return_results/'

transaction_cost_rates = [0.0005, 0.001, 0.0015]
summary_results = []

def data_preparation(df):
    df = df.dropna(subset=['Model_Predicted_Prices'])
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df

def rank_based_allocation(df, return_cols):
    ranks = df[return_cols].rank(axis=1, ascending=False)
    num_stocks = ranks.shape[1]

    top_weight = 0.6
    mid_weight = 0.4
    low_weight = 0.0

    top_threshold = int(num_stocks * 0.2)
    mid_threshold = int(num_stocks * 0.5)

    allocations = np.zeros_like(ranks)

    for i in range(len(ranks)):
        sorted_indices = ranks.iloc[i].sort_values().index.to_list()
        allocations[i, [return_cols.index(col) for col in sorted_indices[:top_threshold]]] = top_weight / top_threshold
        allocations[i, [return_cols.index(col) for col in sorted_indices[top_threshold:mid_threshold]]] = mid_weight / (mid_threshold - top_threshold)
        allocations[i, [return_cols.index(col) for col in sorted_indices[mid_threshold:]]] = low_weight / (num_stocks - mid_threshold)

    return pd.DataFrame(allocations, columns=[col.replace('_Predicted_Return', '_allocation') for col in return_cols], index=df.index)

for folder in folders:
    full_path = signals_path + folder + '/'
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
    log_return_cols = [col.replace('_Predicted_Return', '_log_return') for col in predicted_return_cols]

    allocations = rank_based_allocation(full_df, predicted_return_cols)
    allocation_cols = [col.replace('_log_return', '_allocation') for col in log_return_cols]

    # Portfolio Return without transaction cost
    returns_matrix = full_df[log_return_cols].values
    allocations_matrix = allocations.values
    portfolio_returns_no_cost = np.sum(returns_matrix * allocations_matrix, axis=1)
    cumulative_return_no_cost = np.sum(portfolio_returns_no_cost)

    # Equally Weighted Portfolio cumulative return
    equally_weighted_returns = np.mean(returns_matrix, axis=1)
    cumulative_return_equal_weight = np.sum(equally_weighted_returns)

    # Portfolio Returns with different transaction costs
    cumulative_returns_with_costs = []
    for cost_rate in transaction_cost_rates:
        prev_alloc = allocations.iloc[0].values
        net_returns = []

        for i in range(len(full_df)):
            current_alloc = allocations.iloc[i].values
            port_return = np.sum(returns_matrix[i] * current_alloc)

            if i > 0:
                turnover = np.sum(np.abs(current_alloc - prev_alloc))
                cost = turnover * cost_rate
            else:
                cost = 0.0

            net_return = port_return - cost
            net_returns.append(net_return)
            prev_alloc = current_alloc

        cumulative_net_return = np.sum(net_returns)
        cumulative_returns_with_costs.append(cumulative_net_return)

    # Append to summary
    summary_results.append({
        'Market': folder.upper(),
        'Allocation Return (No Costs)': cumulative_return_no_cost,
        f'Allocation Return (0.05%)': cumulative_returns_with_costs[0],
        f'Allocation Return (0.1%)': cumulative_returns_with_costs[1],
        f'Allocation Return (0.15%)': cumulative_returns_with_costs[2],
        'Equally Weighted Return': cumulative_return_equal_weight
    })

# Create final summary table
summary_df = pd.DataFrame(summary_results)
print(summary_df)

# Optional: save table to CSV
summary_df.to_csv(returns_path + 'portfolio_performance_summary_2.csv', index=False)
