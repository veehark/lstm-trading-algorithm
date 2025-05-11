import glob
import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.optimizers import Adam


folders = ['omxh', 'nse', 'nyse'] 
folder_path = 'C:/Users/vjtha/OneDrive - O365 Turun yliopisto/Pro gradu/data/'
results_path = 'C:/Users/vjtha/OneDrive - O365 Turun yliopisto/Pro gradu/results/signals/'


tresholds = [0.001,0.003,0.005,0.007,0.010]


def prepare_data(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df[['Close', 'Open', 'High', 'Low', 'Volume']])

    
    sequence_length = 60
    x_data = []
    y_data = []

    for i in range(sequence_length, len(scaled_data)):
        x_data.append(scaled_data[i-sequence_length:i, :])
        y_data.append(scaled_data[i, 0])  

    x_data, y_data = np.array(x_data), np.array(y_data)

    
    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2, shuffle=False)

    return x_train, x_test, y_train, y_test, scaler


def create_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dense(units=25))
    model.add(Dense(units=1))
    
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')
    return model


def signals(df,treshold):
    buy_threshold = treshold
    sell_threshold = -treshold
    column_name = 'signals_' + str(treshold)
    df[column_name] = np.where(df['Model_Predicted_Prices'].pct_change() > buy_threshold, 1,
                                 np.where(df['Model_Predicted_Prices'].pct_change() < sell_threshold, -1, 0)
        )
    return df


for folder in folders:
    full_path = folder_path + folder + '/'
    full_results_path = results_path + folder + '/'
    files = [f for f in os.listdir(full_path) if f.endswith('.csv')]

    for file in files:
        try:
            file_path = os.path.join(full_path, file)
            df = pd.read_csv(file_path, sep=';')  
            x_train, x_test, y_train, y_test, scaler = prepare_data(df)
            
            model = create_model((x_train.shape[1], x_train.shape[2]))
            model.fit(x_train, y_train, batch_size=32, epochs=10, verbose=1)

            predictions = model.predict(x_test)
        
            predictions_full = np.zeros((predictions.shape[0], x_test.shape[2]))
            predictions_full[:, 0] = predictions.flatten()
        
            predictions_scaled = scaler.inverse_transform(predictions_full)
            predicted_close_prices = predictions_scaled[:, 0]
        
            df['BuyAndHold_Returns'] = np.log(df['Close'] / df['Close'].shift(1))
        
            df['Model_Signal'] = 0
            df['Model_Predicted_Prices'] = np.nan
    
            test_set_index_start = len(df) - len(y_test)
            
            if len(df) <= test_set_index_start:
                raise ValueError("Index for test set start is out of DataFrame bounds.")
        
            df.loc[df.index[test_set_index_start:], 'Model_Predicted_Prices'] = predicted_close_prices

            for treshold in tresholds:
                df = signals(df,treshold)

            df.to_csv(
                os.path.join(full_results_path, f"{file.split('.')[0]}_signals.csv"),
                index=True
            )
        except:
            df.to_csv(
            os.path.join(full_results_path, f"{file.split('.')[0]}_DOES_NOT_WORK.csv"),
            index=True
            )
            next 