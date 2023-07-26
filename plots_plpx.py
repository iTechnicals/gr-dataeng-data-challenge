import numpy as np
import polars as pl
import plotly.express as px

df = pl.read_csv('data/crypto.csv', try_parse_dates=True)

def standard_plot(currencies = None):
    if not currencies:
        currencies = df['Asset_Name'].unique()
    data = df.filter(pl.col('Asset_Name').is_in(currencies))
    return px.line(x = data['timestamp'], y = data['Close'], color = data['Asset_Name'])

def log_plot(currencies = None):
    if not currencies:
        currencies = df['Asset_Name'].unique()
    data = df.filter(pl.col('Asset_Name').is_in(currencies))
    return px.line(x = data['timestamp'], y = np.log(data['Close']), color = data['Asset_Name'])

def moving_average_plot(period, currencies = None):
    if not currencies:
        currencies = df['Asset_Name'].unique()
    data = df.filter(pl.col('Asset_Name').is_in(currencies)).with_columns(
        moving_average=pl.col('Close').rolling_mean(window_size=period).over('Asset_Name')
    )
    return px.line(x = data['timestamp'], y = data['moving_average'], color = data['Asset_Name'])
        
def stdev_plot(currencies = None):
    if not currencies:
        currencies = list(df['Asset_Name'].unique())
    stdevs = df.groupby('Asset_Name').agg(pl.col('Close').std()/pl.col('Close').mean()).sort('Close')
        
    return px.bar(stdevs, x='Asset_Name', y='Close')

def moving_average_std_plot(period, currencies = None):
    if not currencies:
        currencies = df['Asset_Name'].unique()
    data = df.filter(pl.col('Asset_Name').is_in(currencies)).with_columns(
        moving_std=pl.col('Close').rolling_std(window_size=period).over('Asset_Name')
    )
    return px.line(x = data['timestamp'], y = data['moving_std'], color = data['Asset_Name'])
        
def bollinger(period, currencies = None):
    if not currencies:
        currencies = df['Asset_Name'].unique()
    data = df.filter(pl.col('Asset_Name').is_in(currencies)).with_columns(
        moving_average=pl.col('Close').rolling_mean(window_size=period).over('Asset_Name'),
        moving_std=pl.col('Close').rolling_std(window_size=period).over('Asset_Name')
    )
    return px.line(x = data['timestamp'], y = [data['moving_average'] - 2 * data['moving_std'],
                                               data['moving_average'],
                                               data['moving_average'] + 2 * data['moving_std']], color = data['Asset_Name'])

# log_plot()

# stdev_plot().show()
# moving_average_std_plot(14)

# standard_plot().show()
# moving_average_plot(3).show()

# fig.set_facecolor('#3E4C57')
# ax.set_facecolor('#607687')

bollinger(20, ['Bitcoin']).show()