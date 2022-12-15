from BasePortfolio import BasePortfolio
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import cvxpy as cp
from itertools import combinations

class RobustOptimizationPortfolio(BasePortfolio):
    def __init__(self, coins, prices, start_date, rebalance_period = 'M'):
        super().__init__(coins, prices, start_date, rebalance_period)

    def make_A_matrix(self, returns_df):
        n = len(self.coins)

        A = np.zeros((n*(n-1), n))

        helper_list = list(combinations(range(n), 2))

        for i, (c1, c2) in enumerate(combinations(returns_df.columns, 2)):
            xr_returns = returns_df[c1] / returns_df[c2]

            lb = np.min(xr_returns)
            ub = np.max(xr_returns)

            A[i*2:(i*2)+2,[*helper_list[i]]] = np.array([[1, -lb], [-1, ub]])

        return A
        
    def optimize(self, r, sigma, A, delta=0.1):
        n = len(self.coins)

        w = cp.Variable((n, 1))
        k = cp.Variable((n*(n-1), 1))
        y = cp.Variable((n, 1))

        constraints = [(w >= 0), (k >= 0), (y >= 0), (cp.sum(w) == 1)]

        param_A = cp.Parameter((n*(n-1), n))
        param_A.value = A

        param_r = cp.Parameter((n, 1))
        param_r.value = r.reshape(-1,1)

        prob = cp.Problem(cp.Maximize(param_r.T @ (w-A.T@k-y) - delta*cp.norm(np.power(sigma, 0.5) @(w-A.T@k-y))),
                   constraints)
        
        prob.solve()
        
        return list(w.value)
        
    def calculate_weights(self, rebalance_period, start_date):
        assert rebalance_period in ['M', 'W']
        
        returns = (self.prices/self.prices.shift(1)).dropna()
        
        increment = relativedelta(months=1) if rebalance_period == 'M' else relativedelta(weeks=1)
        
        ts_index = []
        weights = []

        to_add = pd.Timestamp(start_date)

        while to_add < self.prices.index[-1]:
            
            current_returns = returns[:to_add][:-1]
            
            expected_returns = np.array(current_returns.mean())
            covariance = np.array(current_returns.cov())

            A = self.make_A_matrix(current_returns)
            current_weights = self.optimize(expected_returns, covariance, A)
            
            ts_index.append(to_add)
            weights.append(current_weights)
            
            to_add = to_add + increment
        
        return pd.DataFrame(data = weights, 
                                    index=ts_index, 
                                    columns = [f"{coin}USDT" for coin in self.coins])