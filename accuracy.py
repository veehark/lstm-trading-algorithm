import pandas as pd
import os

# Define the folders and paths
folders = ['omxh', 'nse', 'nyse'] 
signals_path = 'C:/Users/vjtha/OneDrive - O365 Turun yliopisto/Pro gradu/results/signals/'
accuracy_path = 'C:/Users/vjtha/OneDrive - O365 Turun yliopisto/Pro gradu/results/accuracy/'

summary_data = []

for folder in folders:
    full_path = os.path.join(signals_path, folder)
    os.makedirs(accuracy_path, exist_ok=True)  # Ensure the output folder exists
    
    files = [f for f in os.listdir(full_path) if f.endswith('_signals.csv')]
    total_positions = 0
    correct_positions = 0
    
    for file in files:
        file_path = os.path.join(full_path, file)
        df = pd.read_csv(file_path)
        
        # Ensure the required columns exist
        if 'Close' in df.columns and 'signals_0.005' in df.columns:
            df['Next_Close'] = df['Close'].shift(-1)  # Get the next day's closing price
            df.dropna(inplace=True)  # Remove last row since it will have NaN in Next_Close
            
            # Compute actual price movement
            df['Actual_Movement'] = df['Next_Close'] - df['Close']
            df['Price_Up'] = df['Actual_Movement'] > 0
            df['Price_Down'] = df['Actual_Movement'] < 0
            
            # Check if signals correctly predicted the movement
            df['Correct_Prediction'] = (
                (df['signals_0.005'] == 1) & df['Price_Up'] |  # Buy when price goes up
                (df['signals_0.005'] == -1) & df['Price_Down']  # Short when price goes down
            )
            
            # Count correct and total positions
            total_positions += (df['signals_0.005'] != 0).sum()
            correct_positions += df['Correct_Prediction'].sum()
    
    # Append summary for each market
    summary_data.append([folder, total_positions, correct_positions])

# Save summary results
summary_df = pd.DataFrame(summary_data, columns=['Market', 'Total Positions', 'Correct Positions'])
summary_file = os.path.join(accuracy_path, 'summary_accuracy.csv')
summary_df.to_csv(summary_file, index=False)

print("Summary file saved successfully.")
