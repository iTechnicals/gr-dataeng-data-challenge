import numpy as np
import polars as pl

df = pl.read_csv('data/crypto.csv')

bitcoin = df.filter(pl.col('Asset_Name') == 'Bitcoin')

expected_value = bitcoin['Close'].mean()
positive_value_count = len(bitcoin.filter(pl.col('Close') > 20000))

print(f'''The average value of Bitcoin over the data set is ${round(expected_value, 2)}.
That means that if you went back to a random date in time and sold a bitcoin you would lose ${round(20000 - expected_value, 2)} on average.
However, your chance of turning a profit would be lower, at {round(100*positive_value_count / bitcoin.shape[0], 2)}%.''')

budget = 20000

for index in range(bitcoin.shape[0] - 1):
    if bitcoin.row(index+1, named=True)['Close'] > bitcoin.row(index, named=True)['Close'] :
        budget *= bitcoin.row(index+1, named=True)['Close'] / bitcoin.row(index, named=True)['Close']

print(f'''With a future-predictor of range 1 day and a budget of 20000, you could make ${round(budget - 20000, 2)}.''')
budget = 20000

for index in range(bitcoin.shape[0] - 1):
    if bitcoin.row(index-6, named=True)['Close'] > bitcoin.row(index, named=True)['Close'] :
        budget *= bitcoin.row(index+1, named=True)['Close'] / bitcoin.row(index, named=True)['Close']

print(f'''With a broken future-predictor of range 1 day and a budget of 20000, you would lose ${round(20000 - budget, 2)}.''')