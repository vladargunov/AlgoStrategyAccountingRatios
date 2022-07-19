


class OLSRatios(Strategy):
    def __init__(self, datamodule):
        super().__init__(datamodule)

        self.reg = LinearRegression()
