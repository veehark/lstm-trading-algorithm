# Introduction

This repository contains code used in the empirical part of the thesis: Stock Market Prediction with Long Short-Term Memory Networks: A Multi-Market Performance Analysis

## Description of the code files

### get_data
Code gets stock data from Yahoo finance 

### generate_signals
Code trains the LSTM model and generate signals based on its predictions during the testing period

### simulate_trading
Code simulates trading using the generated signals and calculates the returns

### analysis
Code compares the results to the benchmark and calculates the excess returns

### plotting_individual_level
Code creates figures for the results

### average_excess 
Code isolates the average excess returns and creates charts to compare them accross signal tresholds and markets

### allocation_met_RBA
Code simulates trading with the rank based allocation strategy using the predictions from the generate_signals code to create the ranking

### allocation_met_RBA_w_cost
Code simulates trading with the rank based allocation strategy while incorporating costs into the trades and creates a table with results

### allocation_met_ERBA
Code simulates trading with the exponential rank based allocation strategy using the predictions from the generate_signals code to create the ranking

### allocation_met_ERBA_w_cost
Code simulates trading with the exponential rank based allocation strategy while incorporating costs into the trades and creates a table with results

### allocation_methods_analysis
Code combines results from allocation_met_RBA and allocation_met_ERBA to compare them with equally weighted portfolio returns

### accuracy
Code calculates the accuracy of the LSTM model's predictions
