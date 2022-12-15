from BasePortfolio import BasePortfolio
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import gurobipy as gp
from gurobipy import GRB

class MinimumVariancePortfolio(BasePortfolio):
    def __init__(self, coins, prices, start_date, rebalance_period = 'M'):
        super().__init__(coins, prices, start_date, rebalance_period)
        
    def optimize(self, r, sigma):
        n = len(self.coins)
        
        model = gp.Model('deterministic portfolio frontier model')
        
        x = model.addMVar(n)
        model.addConstr(x.sum() == 1)

        for i in range(n):
          model.addConstr(x[i] >= 0)

        model.setObjective(x @ sigma @ x,  GRB.MINIMIZE)

        model.optimize()
        
        return x.x
        
    def calculate_weights(self, rebalance_period, start_date):
        assert rebalance_period in ['M', 'W']
        
        # returns = self.prices.pct_change().dropna()
        returns = (self.prices/self.prices.shift(1)).dropna()
        
        increment = relativedelta(months=1) if rebalance_period == 'M' else relativedelta(weeks=1)
        
        ts_index = []
        weights = []

        to_add = pd.Timestamp(start_date)

        while to_add < self.prices.index[-1]:
            
            current_returns = returns[:to_add][:-1]
            
            expected_returns = np.array(current_returns.mean())
            covariance = np.array(current_returns.cov())
            
            current_weights = self.optimize(expected_returns, covariance)
            
            ts_index.append(to_add)
            weights.append(current_weights)
            
            to_add = to_add + increment
        
        return pd.DataFrame(data = weights, 
                                    index=ts_index, 
                                    columns = [f"{coin}USDT" for coin in self.coins])