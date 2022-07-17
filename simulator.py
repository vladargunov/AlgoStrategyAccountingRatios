import numpy as np
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta




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
        """
        self.datamodule = datamodule
        self.portfolio = portfolio
        self.strategy = strategy
        self.frequency = frequency
        self.start_date = start_date
        self.end_date = end_date
        self.dates = self._adjust_available_dates()

        # Metrics
        self.sharpe = 0
        self.return_to_drawdown = 0


    def _adjust_available_dates(self):
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


        # Get first a weekday
        first_date = self.datamodule.choose_weekday(dates_remained[0])


        # Compute the remaining dates of the sample
        selected_dates = [first_date]

        current_date = first_date

        while current_date < dates_remained[-1]:
            current_date = date.fromisoformat(current_date)
            if self.frequency == 'weekly':
                current_date += timedelta(weeks=1)
            elif self.frequency == 'monthly':
                current_date += relativedelta(months=1)
            elif self.frequency == 'yearly':
                current_date += relativedelta(years=1)

            current_weekday = self.datamodule.choose_weekday(current_date)
            while (current_weekday not in dates_remained) and (current_weekday < dates_remained[-1]):
                current_weekday = date.fromisoformat(current_weekday)
                current_weekday += timedelta(days=1)
                current_date = current_weekday
                current_weekday = current_weekday.isoformat()


            selected_dates.append(current_weekday)

            current_date = current_date.isoformat()


        return selected_dates[:-1]


    def simulate(self):
        pass
