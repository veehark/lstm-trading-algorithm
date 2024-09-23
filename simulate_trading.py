
import pandas as pd
import os

folders = ['omxh', 'nse', 'nyse'] 
signals_path = 'C:/Users/vjtha/OneDrive - O365 Turun yliopisto/Pro gradu/results/signals/'
returns_path = 'C:/Users/vjtha/OneDrive - O365 Turun yliopisto/Pro gradu/results/returns/'

tresholds = [0.001,0.003,0.005,0.007,0.010]

def data_preparation(df):
    df = df.dropna(subset=['Model_Predicted_Prices'])
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df

def calculate_returns(df):
    df['cumulative_BnH'] = df['BuyAndHold_Returns'].cumsum()   
    for treshold in tresholds:
        signal_column = 'signals_' + str(treshold)

        return_column = 'returns_' + str(treshold)
        df[return_column] = df['BuyAndHold_Returns'] * df[signal_column]

        cumulative_column = 'cumulative_r_' + str(treshold)
        df[cumulative_column] = df[return_column].cumsum()

        excess_column = 'excess_r_' + str(treshold)
        df[excess_column] = df[cumulative_column] - df['cumulative_BnH']
    return df


for folder in folders:
    full_path = signals_path + folder + '/'
    full_results_path = returns_path + folder + '/'
    files = [f for f in os.listdir(full_path) if f.endswith('_signals.csv')]
    
    for file in files:
        file_path = os.path.join(full_path, file)
        df = pd.read_csv(file_path) 

        df = data_preparation(df)
        
        df = calculate_returns(df)

        df.to_csv(
                os.path.join(full_results_path, f"{file.split('_')[0]}_returns.csv"),
                index=True
            )

