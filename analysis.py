import pandas as pd
import os

folders = ['omxh', 'nse', 'nyse']
returns_path = 'C:/Users/vjtha/OneDrive - O365 Turun yliopisto/Pro gradu/results/returns/'
final_path = 'C:/Users/vjtha/OneDrive - O365 Turun yliopisto/Pro gradu/results/final/'

tresholds = [0.001,0.003,0.005,0.007,0.010]

def data_preparation(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df

for folder in folders:    
    full_path = returns_path + folder + '/'
    files = [f for f in os.listdir(full_path) if f.endswith('_returns.csv')]
    

    for treshold in tresholds:
        excess_returns = pd.DataFrame(columns=['Date']) 
        for file in files:
            file_path = os.path.join(full_path, file)
            df = pd.read_csv(file_path)

            ticker = file.split('_')[0]
            
            excess_name = 'excess_r_' + str(treshold)
            excess_returns = excess_returns.merge(df[['Date', excess_name]], on='Date', how='outer')
            excess_returns.rename(columns={excess_name: ticker}, inplace=True)

        excess_returns['Average'] = excess_returns.iloc[:, 1:].mean(axis=1)
        data_preparation(excess_returns)

        excess_returns.to_csv(final_path + '/' + folder + '/' + 'excess_' + str(treshold) + '.csv')
    
    print(folder + ' done')
    




        
        