

class Portfolio():
    def __init__(self, tickers):
        self.portfolio = {}
        for ticker in tickers:
            self.portfolio[ticker] = 0

        #
        self.total_portfolio = 0


    def get_position(self, ticker):
        assert ticker in self.portfolio.keys(), "No ticker in portfolio!"
        return self.portfolio[ticker]

    def allocate_position(self, ticker, value):
        assert ticker in self.portfolio.keys(), "No ticker in portfolio!"
        self.portfolio[ticker] = value

        
