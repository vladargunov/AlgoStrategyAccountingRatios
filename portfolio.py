

class Portfolio():
    def __init__(self, tickers, name, initial_value=100, max_allocation_long=100, max_allocation_short=100):
        """
        Portfolio class takes the available tickers for the portfolio,
        the initial value of the portfolio, and maximum allocations for
        long and short positions
        """

        self.name = name
        self.portfolio = {}
        self.tickers = tickers
        self.empty_portfolio()

        self.max_allocation_long = max_allocation_long
        self.max_allocation_short = max_allocation_short

        #Value of the portfolio
        self.value = initial_value

    def empty_portfolio(self):
        for ticker in self.tickers:
            # Each value in the dictionary denotes the number of stocks held
            self.portfolio[ticker] = 0
        # Total allocations
        self.total_position_long = 0
        self.total_position_short = 0


    def get_position(self, ticker):
        assert ticker in self.portfolio.keys(), "No ticker in portfolio!"
        return self.portfolio[ticker]

    def allocate_position(self, ticker, value):
        """
        Allocates position to the portfolio and updates total position long
        and total position short
        """
        assert ticker in self.portfolio.keys(), "No ticker in portfolio!"
        prev_value = self.portfolio[ticker]
        change_value = value - prev_value

        # If long
        if value >= 0:
            # Check that value of the portfolio does not exceed maximum allocation
            if (self.total_position_long + change_value) > self.max_allocation_long:
                print('Maximum allocation is reached for long!')
                change_value = self.max_allocation_long - self.total_position_long

            self.total_position_long += change_value
        # If short
        else:
            # Check that value of the portfolio does not exceed maximum allocation
            if (self.total_position_short - change_value) > self.max_allocation_short:
                print('Maximum allocation is reached for short!')
                change_value = self.total_position_short - self.max_allocation_short

            self.total_position_short -= change_value

        # Assign new weight to the portfolio
        self.portfolio[ticker] += change_value


    def update_portfolio(self, price_changes, empty_weights=True):
        """
        Changes the value of the portfolio for each change in prices
        price_changes should be a dictionary with keys of tickers
        and values of changes in prices
        """
        for ticker in self.tickers:
            value_change = price_changes.get(ticker, 0)
            self.value += value_change * self.portfolio.get(ticker,0)

        if empty_weights:
            self.empty_portfolio()

    def __str__(self):
        return (f'Total Value Portfolio: {self.value}\n'
                f'Total Long Position: {self.total_position_long}\n'
                f'Total Short Position: {self.total_position_long}')
