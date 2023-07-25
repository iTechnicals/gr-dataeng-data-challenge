import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/crypto.csv')

def standard_plot(currencies = None):
    if not currencies:
        currencies = df['Asset_Name'].unique()
    for crypto in currencies:
        data = df[df['Asset_Name'] == crypto]
        timestamps = pd.to_datetime(data['timestamp'])
        closing_prices = data['Close']
        plt.plot(timestamps,
                 closing_prices,
                 label=crypto)

def moving_average_plot(period, currencies = None):
    if not currencies:
        currencies = df['Asset_Name'].unique()
    for crypto in currencies:
        data = df[df['Asset_Name'] == crypto]
        timestamps = pd.to_datetime(data['timestamp'])[0:len(timestamps)-period]
        closing_prices = list(data['Close'])
        ma_closing_prices = [sum(closing_prices[i:i+period])/period for i in range(len(closing_prices) - period)]
        plt.plot(timestamps,
                 ma_closing_prices,
                 label=crypto)


standard_plot()
# moving_average_plot(14)
plt.legend()
plt.grid()
plt.show()