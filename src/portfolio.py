

class Portfolio():
    def __init__(self, initial_value=100, max_allocation_long=100, max_allocation_short=100):
        """
        Portfolio class takes the available tickers for the portfolio,
        the initial value of the portfolio, and maximum allocations for
        long and short positions
        """

        self.empty_portfolio()

        # Maximum available shares of long and
        # short of the portfolio (in percentages)
        self.max_allocation_long = max_allocation_long
        self.max_allocation_short = max_allocation_short

        #Value of the portfolio (in amount of money)
        self.value = initial_value

        self.value_cache = [self.value]

    def empty_portfolio(self):
        # Portfolio contains the tickers as keys
        # and the share of the portfolio that it takes as values
        self.portfolio = {}
        # Total allocations
        self.total_position_long = 0
        self.total_position_short = 0


    def get_position(self, ticker):
        assert ticker in self.portfolio.keys(), "No ticker in portfolio!"
        return self.portfolio[ticker]

    def allocate_positions(self, strategy_portfolio):
        """
        Allocates position to the portfolio and updates total position long
        and total position short

        It also assumes that self.portfolio is an empty dict and
        total_position_long and total_position_short are zero
        """
        # Empty the portfolio
        self.empty_portfolio()

        for ticker, position in strategy_portfolio.items():
            # If long
            if position >= 0:
                # Check that value of the portfolio does not exceed maximum allocation
                if (self.total_position_long + position) > self.max_allocation_long:
                    print('Maximum allocation is reached for long!')
                    position = self.max_allocation_long - self.total_position_long

                self.total_position_long += position
            # If short
            else:
                # Check that value of the portfolio does not exceed maximum allocation
                if (self.total_position_short - position) > self.max_allocation_short:
                    print('Maximum allocation is reached for short!')
                    position = self.total_position_short - self.max_allocation_short

                self.total_position_short -= position

            # Assign new weight to the portfolio
            self.portfolio[ticker] = position


    def update_portfolio(self, diff_prices, start_prices):
        """
        Changes the value of the portfolio for each change in prices

        diff_prices should be a dictionary with keys of tickers
        and values of changes in prices
        If the diff_prices does not contain the change in prices for
        the specified ticker, it is assumed that the change in price is zero

        start_prices should be a dictionary with keys of tickers
        and values of changes in prices
        """

        # Record the starting value of the porfolio
        start_value_portfolio = self.value
        for ticker in self.portfolio.keys():
            value_change = diff_prices.get(ticker, 0)
            start_price = start_prices.get(ticker, 0)
            # Change the value by (number of shares) * value change
            self.value += ( self.portfolio.get(ticker,0) *  start_value_portfolio / start_price ) * value_change

        # Add the value of the portfolio to value_cache
        self.value_cache.append(self.value)

    def __str__(self):
        return (f'Total Value Portfolio: {self.value}\n'
                f'Total Long Position: {self.total_position_long}\n'
                f'Total Short Position: {self.total_position_long}')
