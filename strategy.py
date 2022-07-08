from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

from portfolio import Portfolio
from datamodule import DataModule

from sklearn.linear_model import LinearRegression

class Strategy(ABC):
    def __init__(self, datamodule):
        self.dm = datamodule

    @abstractmethod
    def allocate(self, **kwargs):
        pass






class OLSRatios(Strategy):
    def __init__(self):
        super().__init__()

        self.reg = LinearRegression()
