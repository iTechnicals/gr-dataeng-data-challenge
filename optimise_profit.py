import numpy as np
import polars as pl
import pandas as pd
from functools import reduce

df_pd = pd.read_csv('data/crypto.csv')

df = pl.read_csv('data/crypto.csv', try_parse_dates=True)

litecoin = df.filter(pl.col('Asset_Name') == 'Litecoin')
litecoin_pd = df_pd[df_pd['Asset_Name'] == 'Litecoin']
min_price_date = None
max_price_date = None
min_price = np.inf
max_price = 0

min_date = None
max_date = None
min_price_final = np.inf
max_price_final = 0

def reducer_function(x, y):
    if isinstance(x, float):
        x = {'min_price': np.inf,
             'max_price': 0,
             'max_diff': 0}
    x['min_price'] = min(x['min_price'], y)
    if y > x['max_price']:
        x['max_price'] = y
        x['max_diff'] = max(x['max_price'] - x['min_price'], x['max_diff'])
    return x

def aggr(series):
    return reduce(lambda x, y: reducer_function(x, y), series)

print(litecoin_pd['Close'].agg(aggr))

for row in litecoin.iter_rows(named = True):
    if row['Close'] < min_price:
        min_price = row['Close']
        min_price_date = row['timestamp']
    if row['Close'] > max_price:
        max_price = row['Close']
        max_price_date = row['timestamp']
        if max_price - min_price > max_price_final - min_price_final:
            max_price_final = max_price
            min_price_final = min_price
            max_date = max_price_date
            min_date = min_price_date

print(f'''Buy on {min_date} for {min_price_final}.
Sell on {max_date} for {max_price_final} for a profit of {max_price_final - min_price_final} ({round(100*(max_price_final/min_price_final - 1), 2)}%).''')