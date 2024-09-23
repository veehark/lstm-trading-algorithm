import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

folders = ['omxh', 'nse', 'nyse']
final_path = 'C:/Users/vjtha/OneDrive - O365 Turun yliopisto/Pro gradu/results/final/'

tresholds = [0.001,0.003,0.005,0.007,0.01]

def plot_deviation_histogram(df, type):
    last_row = df.iloc[-1, 1:]

    blue = (0.2, 0.4, 0.8)
    red = (0.8, 0.2, 0.2)

    plt.hist(last_row, bins=12, color=blue, edgecolor='black', alpha=0.7)

    average_value = last_row.mean()

    plt.axvline(x=average_value, color=red, linestyle='--', label='Deviation on average')

    plt.xlabel('Values', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title(f'Distribution of Excess Log Returns ({type})', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    #plt.savefig(f'Figures/Final/Distribution_Excess_Returns_{type}.png')
    plt.show()

def plot_deviation_line_chart(df, type):
    df['Average'] = df.iloc[:, 1:].mean(axis=1)
    df['Date'] = pd.to_datetime(df['Date'])
    blue = (0.2, 0.4, 0.8)
    
    for column in df.columns:
        if column != 'Date' and column != 'Average':
            plt.plot(df['Date'], df[column], color=blue, alpha=0.5, label=None, linewidth=0.8) 
    
    plt.plot(df['Date'], df['Average'], color='red', linewidth=1.2)
    
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Values', fontsize=12)
    plt.title(f'Excess Log Returns ({type})', fontsize=14, fontweight='bold')
   
    custom_legend = [Line2D([0], [0], color=blue, lw=2, label='Individual Stocks'),
                     Line2D([0], [0], color='red', lw=2, label='Average Excess Log Returns')]
    plt.legend(handles=custom_legend, loc='lower left', fontsize=10)
    
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    #plt.savefig(f'Figures/Final/Excess_Returns_{type}.png')
    plt.show()

for folder in folders:    
    full_path = final_path + folder + '/'
    for treshold in tresholds:
        files = [f for f in os.listdir(full_path) if f.startswith('excess_'+str(treshold))]
        for file in files:
            file_path = os.path.join(full_path, file)
            df = pd.read_csv(file_path)
            print(df.head())
            plot_deviation_line_chart(df,f"{file} and {folder}")
            plot_deviation_histogram(df,f"{file} and {folder}")