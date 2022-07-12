

class Portfolio():
    def __init__(self, tickers, name):

        self.name = name
        self.portfolio = {}
        for ticker in tickers:
            self.portfolio[ticker] = 0

        # Total allocations
        self.total_position_long = 0
        self.total_position_short = 0

        #Value of the portfolio
        self.value = 1


    def get_position(self, ticker):
        assert ticker in self.portfolio.keys(), "No ticker in portfolio!"
        return self.portfolio[ticker]

    def allocate_position(self, ticker, value):
        assert ticker in self.portfolio.keys(), "No ticker in portfolio!"
        self.portfolio[ticker] = value


    def __str__(self):
        print(f'Total Value Portfolio: {self.value}')
        print(f'Total Long Position: {self.total_position_long}')
        print(f'Total Long Position: {self.total_position_long}')
