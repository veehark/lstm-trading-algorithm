import pandas as pd
import os

# Define the folders and paths
folders = ['omxh', 'nse', 'nyse'] 
signals_path = 'C:/Users/vjtha/OneDrive - O365 Turun yliopisto/Pro gradu/results/signals/'
accuracy_path = 'C:/Users/vjtha/OneDrive - O365 Turun yliopisto/Pro gradu/results/accuracy/'
s_list = ["0.001","0.003","0.005","0.007","0.01"]
summary_data = []
for s1 in s_list:
    for folder in folders:
        full_path = os.path.join(signals_path, folder)
        os.makedirs(accuracy_path, exist_ok=True)  # Ensure the output folder exists
        
        files = [f for f in os.listdir(full_path) if f.endswith('_signals.csv')]
        
        for file in files:
            file_path = os.path.join(full_path, file)
            df = pd.read_csv(file_path)
            
            # Ensure the required columns exist
            if 'Close' in df.columns and f'signals_{s1}' in df.columns:
                df['Prev_Close'] = df['Close'].shift(1)  # Get the previous day's closing price
                df.dropna(inplace=True)  # Remove first row since it will have NaN in Prev_Close
                
                # Compute actual price movement
                df['Actual_Movement'] = df['Close'] - df['Prev_Close']
                df['Price_Up'] = df['Actual_Movement'] > 0
                df['Price_Down'] = df['Actual_Movement'] < 0
                
                # Check if signals correctly predicted the movement
                df['Correct_Prediction'] = (
                    (df[f'signals_{s1}'] == 1) & df['Price_Up'] |  # Buy when price goes up
                    (df[f'signals_{s1}'] == -1) & df['Price_Down']  # Short when price goes down
                )
                
                # Count correct and total positions
                total_positions = (df[f'signals_{s1}'] != 0).sum()
                correct_positions = df['Correct_Prediction'].sum()
                accuracy = correct_positions / total_positions if total_positions > 0 else 0
                
                # Append summary for each stock
                summary_data.append([folder, file, total_positions, correct_positions, accuracy])

    # Save summary results
    summary_df = pd.DataFrame(summary_data, columns=['Market', 'Stock', 'Total Positions', 'Correct Positions', 'Accuracy'])
    summary_file = os.path.join(accuracy_path, f'summary_accuracy_{s1}.csv')
    summary_df.to_csv(summary_file, index=False)
    print(summary_df)
    print("average: ")
    print(summary_df['Accuracy'].mean())
    print("Summary file saved successfully.")
