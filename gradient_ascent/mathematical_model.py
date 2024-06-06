"""Class to create and update the gradient ascent mathematical model."""
import numpy as np



class Model:
    def __init__(self, market_data: object) -> None:
        self.data = market_data


    def gradient(self, x, theta, delta):
        Ft = self.positions(x, theta)
        R = self.returns(Ft, x, delta)
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
        np.random.seed(0)

        theta = np.random.rand(M + 2)
        sharpes = np.zeros(epochs) # store sharpes over time
        
        print("Training model...")

        for i in range(epochs):
            grad, sharpe = self.gradient(x, theta, commission)
            theta = theta + grad * learning_rate

            sharpes[i] = sharpe

            print(f"Epoch {i} - Sharpe: {sharpe}")
        
        print("finished training")
        return theta, sharpes
    

    def train_test_split(self, returns, test_size=0.2):
            x = np.array(returns)

            N = int(
                len(x) * (1 - test_size)
            )
            P = len(x) - N

            x_train = x[-(N+P):-P]
            x_test = x[-P:]

            return self.normalize(x_train), self.normalize(x_test)


    def normalize(self, x):
            std = np.std(x)
            mean = np.mean(x)

            return (x - mean) / std


    def positions(self, x, theta):
        M = len(theta) - 2
        T = len(x)
        Ft = np.zeros(T)
        for t in range(M, T):
            xt = np.concatenate([[1], x[t - M:t], [Ft[t - 1]]])
            Ft[t] = np.tanh(np.dot(theta, xt))
        return Ft


    def returns(self, Ft, x, delta):
        T = len(x)
        rets = Ft[0:T - 1] * x[1:T] - delta * np.abs(Ft[1:T] - Ft[0:T - 1])
        return np.concatenate([[0], rets])

