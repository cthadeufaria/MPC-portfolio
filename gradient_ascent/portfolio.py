import numpy as np



class Portfolio:
    def __init__(self) -> None:
        self.holdings = {}
        self.cash = 0

    def sharpe_ratio(self, returns):
        return returns.mean() / returns.std()
    

    def returns(self, Ft, x, delta):
        T = len(x)
        rets = Ft[0:T - 1] * x[1:T] - delta * np.abs(Ft[1:T] - Ft[0:T - 1])
        return np.concatenate([[0], rets])
    

    def positions(self, x, theta):
        M = len(theta) - 2
        T = len(x)
        Ft = np.zeros(T)
        for t in range(M, T):
            xt = np.concatenate([[1], x[t - M:t], [Ft[t - 1]]])
            Ft[t] = np.tanh(np.dot(theta, xt))
        return Ft

