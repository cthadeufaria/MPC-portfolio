import numpy as np

from gradient_ascent.mathematical_model import Model



class Portfolio(Model):
    def __init__(self, assets: dict, available: float) -> None:
        self.assets = assets
        self.available = available


    def sharpe_ratio(self, returns: np.array) -> float:
        return returns.mean() / returns.std()