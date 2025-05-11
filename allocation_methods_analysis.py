import pandas as pd
import matplotlib.pyplot as plt

# Correct file path to your Excel file
file_path = r"C:\Users\vjtha\OneDrive - O365 Turun yliopisto\Pro gradu\results\allocation_return_results\allocation results summarized.xlsx"

# List of sheets you want to plot
sheets = ['nse', 'nyse', 'omxh']

# Loop through each sheet to read the data and plot the time series separately
for sheet in sheets:
    # Read the data from the current sheet
    df = pd.read_excel(file_path, sheet_name=sheet)
    
    # Convert the 'Date' column to datetime type
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')

    # Plot the time series
    plt.figure(figsize=(10, 6))
    plt.plot(df['Date'], df[f'{sheet} exp'], label='Exponential', color='orange', linewidth=1)
    plt.plot(df['Date'], df[f'{sheet} ew'], label='Equally Weighted', color='black', linewidth=1)
    plt.plot(df['Date'], df[f'{sheet} rank'], label='Rank', color='blue', linewidth=1)

    # Adding title and labels
    plt.title(f"Cumulative Logarithmic Returns for Different Allocation Strategies in {sheet.upper()}", fontsize=14)
    plt.xlabel('Date')
    plt.ylabel('Cumulative Logarithmic Return')
    
    # Show the legend and grid
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Show the plot
    plt.show()
