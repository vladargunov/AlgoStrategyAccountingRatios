import numpy as np
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from tqdm import tqdm
import os
import joblib


class Simulator():

    def __init__(self, datamodule, portfolio, strategy, frequency='daily',
                             start_date='2005-01-04', end_date='2022-05-11'):
        """
        Simulator class for backtesting various strategies and computing the
        required metrics

        Comment on frequencies:
        If frequency is daily, then choose all available dates
        If frequency is weekly, data appears on each 7th day from the start date,
        if the weekday is selected, otherwise the next monday is used as a first day
        If frequency is monthly, data appears for each same day of the month if it is weekday,
        otherwise the next from the selected monday is chosen
        If frequency is yearly, data appears for each date of the year from the first date
        if it is weekday, otherwise choose the next monday

        Comment on missing dates in the data:
        If the selected date by the simulator is not available,
        then the nearest available date is chosen and the trading interval
        follows from such date

        Comment on self.strategy.required_number_dates:
        The simulator will not execute anything until the self.dates
        will contain the sufficient number of time observations as required by
        self.strategy in self.strategy.required_number_dates.
        That is, there will be a warm up period from the start date by the number of
        intervals defined by self.strategy.required_number_dates
        """
        self.datamodule = datamodule
        self.portfolio = portfolio
        self.strategy = strategy
        self.frequency = frequency
        self.start_date = start_date
        self.end_date = end_date
        self.dates = self.get_available_dates()

        # Metrics
        self.sharpe = None
        self.return_to_drawdown = None



    def get_available_dates(self):
        """
        Gets available dates at which the stocks can be traded and
        adjust the datamodule
        """
        assert self.frequency in ['daily', 'weekly', 'monthly', 'yearly'], ('Warning, '
                                                     'frequency is chosen incorrectly!')

        dates_remained = self.datamodule._get_dates(ticker='all', start_date=self.start_date,
                                                    end_date=self.end_date)

        if self.frequency == 'daily':
            return list(dates_remained)

        # Get first a date
        first_date = dates_remained[0]

        # Compute the remaining dates of the sample
        selected_dates = [first_date]
        current_date = first_date

        # Conditions are checked in isoformat
        while current_date < dates_remained[-1]:
            current_date = date.fromisoformat(current_date)
            if self.frequency == 'weekly':
                current_date += timedelta(weeks=1)
            elif self.frequency == 'monthly':
                current_date += relativedelta(months=1)
            elif self.frequency == 'yearly':
                current_date += relativedelta(years=1)

            check_date = current_date.isoformat()
            while (check_date not in dates_remained) and (check_date < dates_remained[-1]):
                current_date += timedelta(days=1)
                check_date = current_date.isoformat()

            # Append current_date in isoformat
            current_date = current_date.isoformat()
            selected_dates.append(current_date)

        return selected_dates[:-1]


    def simulate(self, verbose=True):

        for idx, date in enumerate(tqdm(self.dates, desc='Simulation in progress', ncols=100)):
            if (idx < self.strategy.required_number_dates) or (date == self.dates[-1]):
                continue
            # Returns the strategy data that is needed to create a portfolio for dates
            # before the current_date
            strategy_data = self.datamodule._get_trailing_data(
                                            dates=self.dates,
                                            number_previous_dates=self.strategy.required_number_dates,
                                            current_date=date
                                                                )

            # Get tickers that are available to trade at the current_date
            available_tickers = self.datamodule.get_tickers(date)
            # Returns a dictionary of allocated weights to available tickers
            strategy_portfolio = self.strategy.create_portfolio(strategy_data, available_tickers)

            # Allocates the positions from strategy_portfolio to portfolio
            self.portfolio.allocate_positions(strategy_portfolio)

            # Change the portfolio based on the latest prices
            diff_prices, start_prices = self.datamodule.get_diff_and_current_prices(available_tickers,
                                                   self.dates[(idx-1)], self.dates[idx])

            self.portfolio.update_portfolio(diff_prices, start_prices)

        if verbose:
            print('...Printing the portfolio history...')
            print('-' * 24)
            print('|' + ' ' * 12 + '|' + ' ' * 9 + '|' )
            print('|    Date    |  Value  |')
            print('|' + ' ' * 12 + '|' + ' ' * 9 + '|' )
            print('-' * 24)
            for date, value in zip(self.dates[self.strategy.required_number_dates:],
                                   self.portfolio.value_cache):
                                   print(f'| {date} | {value:6.2f}  |')
            print('-' * 24)


    def compute_metrics(self, risk_free_rate=.01, verbose=True):
        # Return to Drawdown
        self.return_to_drawdown = self.portfolio.value_cache[-1] / min(self.portfolio.value_cache)

        # Sharpe
        excess_return = np.array([(val / self.portfolio.value_cache[0] - 1) for val
                                in self.portfolio.value_cache[1:]]) - risk_free_rate
        mean = np.mean(excess_return)
        stdev = np.std(excess_return)
        self.sharpe = mean / stdev

        if verbose:
            print(f'Sharpe: {self.sharpe:.2f}')
            print(f'Return to Drawdown: {self.return_to_drawdown:.2f}')

    def save_history(self, file_path='src/strategies/trade_history/history.gz'):

        key = '_'.join([repr(self.strategy), self.frequency, self.start_date, self.end_date])
        current_history = {'history_portfolio' : self.portfolio.value_cache, 'sharpe' : self.sharpe,
                           'return_to_drawdown' : self.return_to_drawdown}

        if not os.path.exists(file_path):
            history = {key : current_history}
            joblib.dump(history, file_path)
        else:
            history = joblib.load(file_path)
            history[key] = current_history
            
        print(f'Current model is saved to {file_path} with the key {key}')
