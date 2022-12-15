import re
import numpy as np
import pandas as pd
from datetime import timedelta

class BasePortfolio:
    def __init__(self, coins, prices, start_date, rebalance_period = 'M'):
        assert rebalance_period in ['M', 'W']
        
        self.name = ' '.join(re.sub( r"([A-Z])", r" \1", self.__class__.__name__).split())
        
        self.coins = coins
        self.prices = prices
        self.start_date = start_date
        self.rebalance_period = rebalance_period
        
        self.weights = self.calculate_weights(self.rebalance_period, start_date)
        
    def calculate_weights(self, rebalance_period, start_date):
        raise NotImplementedError
        
    def backtest(self, starting_cash = 1):
        self.portfolio_usd_value = pd.DataFrame(index = self.prices.loc[self.weights.index[0]:].index, columns = self.prices.columns)
        
        print(f"Running backtest on {self.name} with rebalancing period '{self.rebalance_period}' and initial cash of ${starting_cash}")
        
        curr_usd_value = starting_cash

        for i, ts in enumerate(self.portfolio_usd_value.index):
            prev_ts = ts - timedelta(hours=1)
            if ts in self.weights.index:
                if i != 0:
                    self.portfolio_usd_value.loc[ts] = self.prices.loc[ts] / self.prices.loc[prev_ts] * self.portfolio_usd_value.loc[prev_ts]
                    curr_usd_value = self.portfolio_usd_value.loc[ts].sum()

                self.portfolio_usd_value.loc[ts] = self.weights.loc[ts] * curr_usd_value

            else:
                self.portfolio_usd_value.loc[ts] = self.prices.loc[ts] / self.prices.loc[prev_ts] * self.portfolio_usd_value.loc[prev_ts]
                curr_usd_value = self.portfolio_usd_value.loc[ts].sum()
                
        return self.portfolio_usd_value
    
    def plot(self):
        if not 'portfolio_usd_value' in dir(self):
            raise AssertionError("Please run backtest() method first")
            
        fig = self.portfolio_usd_value.sum(axis=1).plot()
        fig.set_title(f'{self.name}: Portfolio value in USD')
        fig.set_xlabel('Date')
        fig.set_ylabel('Portfolio value')
        
        return fig
    
    def get_metrics(self):
        if not 'portfolio_usd_value' in dir(self):
            raise AssertionError("Please run backtest() method first")
            
        total_portfolio = self.portfolio_usd_value.sum(axis=1)
        returns = total_portfolio.pct_change()
        
        ann_mean = returns.mean() * 24 * 365
        ann_std_dev = returns.std() * np.sqrt(24 * 365)
        downside_std = returns[returns < 0].std() * np.sqrt(24 * 365)

        sharpe_ratio = ann_mean / ann_std_dev
        sortino_ratio = ann_mean / downside_std
        max_drawdown = (total_portfolio/total_portfolio.cummax() - 1.0).min()
        diversification_metric = (self.portfolio_usd_value.std(axis=1) / total_portfolio).mean()
        
        return {"Annualized mean": ann_mean,
                "Annualized std. dev.": ann_std_dev,
                "Sharpe ratio": sharpe_ratio,
                "Sortino ratio": sortino_ratio,
                "Max drawdown": max_drawdown,
                "Diversification metric": diversification_metric
               }