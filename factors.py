import pdb
from datetime import date

import pandas as pd
import numpy as np
import alphalens

from const import market_dtypes, market_date_cols, news_dtypes, news_date_cols

MARKET_FP = 'raw/small_market.csv'
NEWS_FP = 'raw/small_newsdata.csv'


class FactorLab():
    def __init__(self):
        self.df_market_orig = pd.read_csv(
            MARKET_FP, dtype=market_dtypes, parse_dates=market_date_cols)
        self.df_news_orig = pd.read_csv(
            NEWS_FP, dtype=news_dtypes, parse_dates=news_date_cols)
        self.universe = self.df_market_orig['assetCode'].unique().tolist()

    def get_pricing(self, col='open', start=None, end=None):
        df_market = self.df_market_orig.copy()
        df_market['time'] = df_market['time'].dt.date
        if start:
            df_market = df_market[df_market['time'] >= start]
        if end:
            df_market = df_market[df_market['time'] <= end]
        df_market = df_market[['time', 'assetCode', col]]
        series_list = list()
        for di, df in df_market.groupby(['time']):
            df = df[['assetCode', 'open']]
            df.set_index('assetCode', inplace=True)
            df.columns = [di]  # TODO find better ways
            series_list.append(df[di])
        return pd.concat(series_list, axis=1).transpose()

    def random_factor(self, start, end, lower, upper):
        pass


if __name__ == "__main__":
    start = date(2007, 3, 1)
    end = date(2020, 3, 2)
    lab = FactorLab()
    df = lab.get_pricing(start=start, end=end)
    pdb.set_trace()
