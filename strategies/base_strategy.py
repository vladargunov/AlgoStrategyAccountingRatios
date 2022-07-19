from abc import ABC, abstractmethod


class BaseStrategy(ABC):
    """
    A BaseStrategy class that must be a parent class for any other
    strategy. All child strategies mist be defined in the following way

    class TestStrategy(BaseStrategy):
        def __init__(self, **kwargs):
            super().__init__(required_number_dates=***)
            # Some code

        def create_portfolio(self, strategy_data)  -> dict:
            # Some code
    """
    def __init__(self, requires_diff_data=None, required_number_dates=None):
        self.requires_diff_data = requires_diff_data
        self.required_number_dates = required_number_dates

        if (self.required_number_dates == None) or (self.required_number_dates <= 1):
            raise NotImplementedError('Strategy must set the value for required_number_dates (int >= 2)!')

    @abstractmethod
    def create_portfolio(self, strategy_data) -> dict:
        pass


class TestStrategy(BaseStrategy):
    def __init__(self, **kwargs):
        super().__init__(required_number_dates=2)


    def create_portfolio(self, strategy_data) -> dict:
        return {'sh600000' : 1}
