from BasePortfolio import BasePortfolio
from dateutil.relativedelta import relativedelta
import pandas as pd

class EqualWeightedPortfolio(BasePortfolio):
    def __init__(self, coins, prices, start_date, rebalance_period = 'M'):
        super().__init__(coins, prices, start_date, rebalance_period)
        
    def calculate_weights(self, rebalance_period, start_date):
        assert rebalance_period in ['M', 'W']
        
        increment = relativedelta(months=1) if rebalance_period == 'M' else relativedelta(weeks=1)
        
        ts_index = []

        to_add = pd.Timestamp(start_date)

        while to_add < self.prices.index[-1]:
            ts_index.append(to_add)

            to_add = to_add + relativedelta(months=1)
            
        return pd.DataFrame(data = 1/len(self.coins), 
                                    index=ts_index, 
                                    columns = [f"{coin}USDT" for coin in self.coins])