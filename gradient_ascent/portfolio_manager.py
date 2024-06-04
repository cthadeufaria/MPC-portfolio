from gradient_ascent.portfolio import Portfolio
import numpy as np



class Manager:
    def __init__(self, portfolio):
        self.portfolio = self.add_portfolio()


    def positions(x, theta):
        M = len(theta) - 2
        T = len(x)
        Ft = np.zeros(T)
        for t in range(M, T):
            xt = np.concatenate([[1], x[t - M:t], [Ft[t - 1]]])
            Ft[t] = np.tanh(np.dot(theta, xt))
        return Ft


    def add_portfolio(self):
        return Portfolio()