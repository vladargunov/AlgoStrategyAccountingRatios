from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

from portfolio import Portfolio
from datamodule import DataModule

from sklearn.linear_model import LinearRegression

class Strategy(ABC):
    def __init__(self, datamodule):
        # Module should be put at init to ensure what data can be used
        self.dm = datamodule

    @abstractmethod
    def allocate(self, **kwargs):
        pass






class OLSRatios(Strategy):
    def __init__(self, datamodule):
        super().__init__(datamodule)

        self.reg = LinearRegression()
