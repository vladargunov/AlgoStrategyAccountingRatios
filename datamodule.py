import numpy as np
import pandas as pd


class DataModule():
    def __init__(self, path_data):
        self.tickers = pd.read_csv('./data/ticker_info.csv')['ticker'].unique()
        self.data = pd.read_csv('./data/stock_data.csv')


    def delete_stocks(self, stocks):
        self.tickers = np.delete(self.tickers, stocks)
        print(f'Deleted {len(sotcks)} stocks')
        print(f'Remaining number of stocks: {len(self.tickers)}')


    def get_tickers(self):
        print('...Returning Tickers...')
        print(f'Total available stocks: {len(self.tickers)}')
        return self.tickers


    def get_prices(self, ticker, start_date='2005-01-04', end_date='2022-05-11'):
        return (self.data[(self.data['ticker'] == ticker) && (self.data['date'] >= start_date)
                && (self.data['date'] <= end_date)]['open'] +
                self.data[(self.data['ticker'] == ticker) && (self.data['date'] >= start_date)
                && (self.data['date'] <= end_date)]['close']) / 2
