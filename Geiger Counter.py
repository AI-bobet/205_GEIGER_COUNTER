# %%
import time
start_time = time.time()
from datetime import datetime
import pandas as pd
import pandas_ta as ta
import logging
from tvDatafeed import TvDatafeed, Interval
import multiprocessing as mp

logging.basicConfig(level=logging.DEBUG)
date_today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

tv = TvDatafeed()

# %%
# major fiat currencies
fiat_currencies = [{'ticker': 'USD', 'currency': 'US Dollar', 'strength': 0},
                   {'ticker': 'EUR', 'currency': 'Euro', 'strength': 0},
                   {'ticker': 'JPY', 'currency': 'Japanese Yen', 'strength': 0},
                   {'ticker': 'GBP', 'currency': 'Pound Sterling', 'strength': 0},
                   {'ticker': 'CHF', 'currency': 'Swiss Franc', 'strength': 0},
                   {'ticker': 'CAD', 'currency': 'Canadian Dollar', 'strength': 0},
                   {'ticker': 'AUD', 'currency': 'Australian Dollar', 'strength': 0},
                   {'ticker': 'NZD', 'currency': 'New Zealand Dollar', 'strength': 0}]

# fiat currency pairs available in OANDA
fiat_pairs = ['AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD', 'AUDUSD', 'CADCHF', 'CADJPY',
              'CHFJPY', 'EURAUD', 'EURCAD', 'EURCHF', 'EURGBP', 'EURJPY', 'EURNZD',
              'EURUSD', 'GBPAUD', 'GBPCAD', 'GBPCHF', 'GBPJPY', 'GBPNZD', 'GBPUSD',
              'NZDCAD', 'NZDCHF', 'NZDJPY', 'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY']

# %%

cur_meter = pd.DataFrame(fiat_currencies).set_index('ticker')
# scrap data from tradingview
for x in fiat_pairs:
    try:
        df = tv.get_hist(x, 'OANDA', interval=Interval.in_weekly, n_bars=16)
        # calculate the % change during the last 15-weeks
        ind = float(ta.roc(close=df['close'], length=15).dropna().values)
        if ind > 0:
            cur_meter.at[x[:3], 'strength'] = cur_meter.at[x[:3], 'strength']+1
            # inverse currency
            cur_meter.at[x[3:], 'strength'] = cur_meter.at[x[3:], 'strength']-1
        else:
            cur_meter.at[x[:3], 'strength'] = cur_meter.at[x[:3], 'strength']-1
            # inverse currency
            cur_meter.at[x[3:], 'strength'] = cur_meter.at[x[3:], 'strength']+1

    except AttributeError:
        pass
# rank from strongest to weakest
cur_meter['Rank'] = cur_meter['strength'].rank(ascending=False)
print(cur_meter.reset_index().sort_values(by=['Rank']).set_index('Rank'))

"{0} mins has lapsed".format(((time.time()-start_time)/60))

# %%
