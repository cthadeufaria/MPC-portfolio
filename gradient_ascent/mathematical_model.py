from gradient_ascent.portfolio import Portfolio
import numpy as np



class Model:
    def __init__(self):
        pass

    def gradient(self, x, theta, delta, positions, returns):
        Ft = positions(x, theta)
        R = returns(Ft, x, delta)
        T = len(x)
        M = len(theta) - 2
        
        A = np.mean(R)
        B = np.mean(np.square(R))
        S = A / np.sqrt(B - A ** 2)

        dSdA = S * (1 + S ** 2) / A
        dSdB = -S ** 3 / 2 / A ** 2
        dAdR = 1. / T
        dBdR = 2. / T * R
        
        grad = np.zeros(M + 2)  # initialize gradient
        dFpdtheta = np.zeros(M + 2)  # for storing previous dFdtheta
        
        for t in range(M, T):
            xt = np.concatenate([[1], x[t - M:t], [Ft[t-1]]])
            dRdF = -delta * np.sign(Ft[t] - Ft[t-1])
            dRdFp = x[t] + delta * np.sign(Ft[t] - Ft[t-1])
            dFdtheta = (1 - Ft[t] ** 2) * (xt + theta[-1] * dFpdtheta)
            dSdtheta = (dSdA * dAdR + dSdB * dBdR[t]) * (dRdF * dFdtheta + dRdFp * dFpdtheta)
            grad = grad + dSdtheta
            dFpdtheta = dFdtheta

            
        return grad, S


    def train(self, x, epochs=2000, M=8, commission=0.0025, learning_rate = 0.3):
        theta = np.random.rand(M + 2)
        sharpes = np.zeros(epochs) # store sharpes over time
        for i in range(epochs):
            grad, sharpe = self.gradient(x, theta, commission)
            theta = theta + grad * learning_rate

            sharpes[i] = sharpe
        
        
        print("finished training")
        return theta, sharpes
    

    def train_test_split(self, returns, test_size=0.2):
            x = np.array(returns)

            N = len(x) * (1 - test_size)
            P = 200 * test_size
            x_train = x[-(N+P):-P]
            x_test = x[-P:]

            std = np.std(x_train)
            mean = np.mean(x_train)

            x_train = (x_train - mean) / std
            x_test = (x_test - mean) / std

            return x_train, x_test

