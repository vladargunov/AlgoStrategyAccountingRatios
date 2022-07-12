from abc import ABC, abstractmethod


from portfolio import Portfolio
from datamodule import DataModule

class BaseStrategy(ABC):
    def __init__(self, datamodule):
        # Module should be put at init to ensure what data can be used
        self.dm = datamodule

    @abstractmethod
    def allocate(self, **kwargs):
        pass
