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

def log_plot(currencies = None):
    if not currencies:
        currencies = df['Asset_Name'].unique()
    for crypto in currencies:
        data = df[df['Asset_Name'] == crypto]
        timestamps = pd.to_datetime(data['timestamp'])
        closing_prices = data['Close']
        plt.plot(timestamps,
                 np.log(closing_prices),
                 label=crypto + ' log')

def moving_average_plot(period, currencies = None):
    if not currencies:
        currencies = df['Asset_Name'].unique()
    for crypto in currencies:
        data = df[df['Asset_Name'] == crypto]
        timestamps = pd.to_datetime(data['timestamp'])
        timestamps = timestamps.iloc[:-period]
        closing_prices = data['Close']
        ma_closing_prices = closing_prices.rolling(period).mean().iloc[period:]
        plt.plot(timestamps,
                 ma_closing_prices,
                 label=crypto + ' smoothed')
        
def stdev_plot(currencies = None):
    if not currencies:
        currencies = list(df['Asset_Name'].unique())
    stdevs = []
    stdevdict = {}
    for crypto in currencies:
        data = df[df['Asset_Name'] == crypto]
        std = data['Close'].std()
        mean = data['Close'].mean()
        stdevs.append(std/mean)
        stdevdict[crypto] = std/mean

    currencies.sort(key = lambda x: stdevdict[x])
    stdevs.sort()
        
    plt.bar(currencies, stdevs)

def moving_average_std_plot(period, currencies = None):
    if not currencies:
        currencies = df['Asset_Name'].unique()
    for crypto in currencies:
        data = df[df['Asset_Name'] == crypto]
        timestamps = pd.to_datetime(data['timestamp'])
        timestamps = timestamps.iloc[:-period]
        closing_prices = data['Close']
        closing_prices_std = closing_prices.rolling(period).std().iloc[period:]
        plt.plot(timestamps,
                 closing_prices_std,
                 label=crypto + ' standard deviation')
        
def bollinger(period, mid_colour, edge_colour, currencies = None):
    if not currencies:
        currencies = df['Asset_Name'].unique()
    for crypto in currencies:
        data = df[df['Asset_Name'] == crypto]
        timestamps = pd.to_datetime(data['timestamp'])
        timestamps = timestamps.iloc[period:]
        closing_prices = data['Close']
        ma_closing_prices = closing_prices.rolling(period).mean().iloc[period:]
        closing_prices_std = closing_prices.rolling(period).std().iloc[period:]
        plt.plot(timestamps,
                 ma_closing_prices + 2 * closing_prices_std,
                 label=crypto + ' +2stdev',
                 color=edge_colour)
        plt.plot(timestamps,
                 ma_closing_prices,
                 label=crypto + ' moving avg',
                 color=mid_colour)
        plt.plot(timestamps,
                 ma_closing_prices - 2 * closing_prices_std,
                 label=crypto + ' -2stdev',
                 color=edge_colour)


fig, ax = plt.subplots()

# log_plot()

# stdev_plot()
# moving_average_std_plot(14)

# standard_plot(['Bitcoin'])
moving_average_plot(20)

# fig.set_facecolor('#3E4C57')
# ax.set_facecolor('#607687')

# bollinger(20, "#00CCCC", "#007D7D", ['Bitcoin'])

plt.legend()
plt.grid()
plt.show()