import numpy as np
import pandas as pd
import datetime
from datetime import date, timedelta


class DataModule():
    start_date_datamodule = '2005-01-04'

    def __init__(self):
        self.tickers = pd.read_csv('data/ticker_info.csv')['ticker'].unique()
        self.data = self._get_data()
        self.features = ['open', 'high', 'low', 'close', 'volume', 'outstanding_share',
                         'turnover', 'pe', 'pe_ttm', 'pb', 'ps', 'ps_ttm', 'dv_ratio',
                          'dv_ttm', 'total_mv', 'qfq_factor']

    def _get_data(self):
        data = pd.read_csv('data/stock_data.csv')
        data['price'] = (data['open'] + data['close']) / 2
        return data


    def delete_stocks(self, stocks):
        self.tickers = np.delete(self.tickers, stocks)
        print(f'Deleted {len(sotcks)} stocks')
        print(f'Remaining number of stocks: {len(self.tickers)}')


    def get_tickers(self, date):
        return self.data[self.data['date'] == date]['ticker'].unique()


    def _get_dates(self, ticker, start_date, end_date):
        """
        Returns a numpy array of dates
        """
        if ticker == 'all':
            dates = self.data[ ( self.data['date'] >= start_date )
                    & ( self.data['date'] <= end_date )]['date'].to_numpy()
        else:
            dates = self.data[( self.data['ticker'] == ticker ) & ( self.data['date'] >= start_date )
                    & ( self.data['date'] <= end_date )]['date'].to_numpy()

        return dates

    @staticmethod
    def choose_weekday(selected_date):
        """
        Accepts both isoformat and date format
        If weekday, gets the same date
        If weekend, returns the next monday
        Returns everything in the format "yyyy-mm-dd"
        """
        if isinstance(selected_date, str):
            selected_date = date.fromisoformat(selected_date)

        assert isinstance(selected_date, datetime.date), ('Warning, selected date'
                                                  'is not a datetime.date format!')

        if selected_date.isoweekday() == 6:
            selected_date += timedelta(days=2)
        elif selected_date.isoweekday() == 7:
            selected_date += timedelta(days=1)

        assert selected_date.isoweekday() <= 5, 'Warning, first date is chosen to be a weekend!'
        return selected_date.isoformat()

    def _keep_dates(self, dates):
        """
        Keeps given dates from the datamodule and delete everything else
        """
        self.data = self.data[~self.data['date'].isin(dates)]

    def get_diff_and_current_prices(self, tickers, start_date, end_date):
        """
        Returns diff prices of all specified tickers over the date interval specified
        by start_date, end_date. Also returns prices at the start_date
        ticker : tickers of the stocks to be chosen
        start_date
        end_date
        """
        assert set(tickers).issubset(self.tickers), "Warning! Some tickers are not available."

        prices_start = self.data[( self.data['ticker'].isin(tickers) ) &
                        ( self.data['date'] == start_date )][['ticker', 'price']]
        prices_start.set_index('ticker', inplace=True)

        prices_end = self.data[( self.data['ticker'].isin(tickers) ) &
                        ( self.data['date'] == end_date )][['ticker', 'price']]
        prices_end.set_index('ticker', inplace=True)

        prices_diff = prices_end.subtract(prices_start).dropna()

        return prices_diff.to_dict()['price'], prices_start.to_dict()['price']

    def _get_trailing_data(self, dates, number_previous_dates, current_date):
        """
        Gets the trailing data for number_previous_dates time periods from current dates
        over dates.
        """
        index_current_date = dates.index(current_date)
        required_dates = dates[max(index_current_date - number_previous_dates, 0):index_current_date]

        return self.data[self.data['date'].isin(required_dates)]

    def get_feature(self, ticker, feature, start_date='2005-01-04', end_date='2022-05-11',
                    days_from_end_date=None, verbose=False):

        assert ticker in self.tickers, "Warning! Ticker is not available."
        assert feature in self.features, "Warning! Feature is not available."

        dates = self._get_dates(ticker, start_date, end_date, days_from_end_date)

        values = self.data[( self.data['ticker'] == ticker ) &
                 ( self.data['date'].isin(dates) )][feature].to_numpy()

        if verbose:
            print(f'Ticker: {ticker}')
            print(f'Start date: {dates[0]}')
            print(f'Total days available: {len(dates)}')
            print(f'Returned feature {feature}')

        return values, dates


    def print_info(self):
        print('Start date: 2005-01-04')
        print('End date: 2022-05-11')
        print(f'Total available stocks: {len(self.tickers)}')

    @staticmethod
    def print_available_features():
        print('open : The open price of the trading day\n' \
              'close : The close price of the trading day\n' \
              'high : The highest price of the trading day\n' \
              'low : The lowest price of the trading day\n' \
              'volume : The trading volume of the trading day\n' \
              'outstanding_share : A company\'s stock currently held by all its shareholders\n' \
              'turnover : A measure of stock liquidity, calculated by dividing the total number of ' \
              'shares traded during the trading day by the ' \
              'average number of shares outstanding for the same trading day.\n' \
              'pe : PE (price to earnings) ratio\n' \
              'pe_ttm : Trailing Twelve Months PE ratio: the current share price divided by the' \
              'last 4 quarterly EPS (earnings per share).\n' \
              'pb : PB ratio (price to book ratio)\n' \
              'ps : PS ratio (price to sales ratio)\n' \
              'ps_ttm : Trailing 12 months PS ratio\n' \
              'dv_ratio : Dividend yield ratio (the percentage of a company\'s '
              'share price that it pays out)\n' \
              'dv_ttm : Trailing 12 months Dividend yield ratio\n' \
              'total_mv : Total market capitalization\n' \
              'qfq_factor : The price adjustment factor')
