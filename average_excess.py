import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

# Set the main directory (no need for raw string, just use double backslashes)
root_path = 'C:\\Users\\vjtha\\OneDrive - O365 Turun yliopisto\\Pro gradu\\results\\final'

# Subfolders to process
folders = ['omxh', 'nyse', 'nse']

# Create 'averages' folder if it doesn't exist
averages_folder = os.path.join(root_path, 'averages')
os.makedirs(averages_folder, exist_ok=True)

for folder in folders:
    folder_path = os.path.join(root_path, folder)
    plt.figure(figsize=(10, 6))
    files_found = False

    # Find all CSV files that start with "excess_" and end in ".csv"
    pattern = os.path.join(folder_path, 'excess_*.csv')
    file_list = glob.glob(pattern)

    for filepath in sorted(file_list):
        try:
            filename = os.path.basename(filepath)
            suffix = filename.replace('excess_', '').replace('.csv', '')  # Extract '0.001' etc.

            df = pd.read_csv(filepath)
            x = df.index  # Change to df['Time'] if you have time column
            y = df['Average']

            plt.plot(x, y, label=suffix)
            files_found = True
        except Exception as e:
            print(f'Error reading {filepath}: {e}')

    if files_found:
        plt.title(f'Average Excess Returns Comparison for {folder.upper()}')
        plt.xlabel('Time')
        plt.ylabel('Average')
        plt.legend(title='Signal sensitivity')
        plt.grid(True)
        plt.tight_layout()

        output_file = os.path.join(averages_folder, f'{folder}_average_comparison.png')
        plt.savefig(output_file)
        print(f'Saved plot: {output_file}')
    else:
        print(f'No valid files found in {folder_path}')
