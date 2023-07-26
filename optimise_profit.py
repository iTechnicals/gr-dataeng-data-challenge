import numpy as np
import polars as pl

df = pl.read_csv('data/crypto.csv', try_parse_dates=True)

litecoin = df.filter(pl.col('Asset_Name') == 'Litecoin')
min_price_date = None
max_price_date = None
min_price = np.inf
max_price = 0

min_date = None
max_date = None
min_price_final = np.inf
max_price_final = 0

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