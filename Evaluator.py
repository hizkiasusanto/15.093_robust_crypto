import matplotlib.pyplot as plt
import pandas as pd

class Evaluator:
    def __init__(self, portfolio_objects):
        self.portfolio_objs = portfolio_objects

    def plot(self):
        fig, ax = plt.subplots(1, figsize=(10,4))

        ax.set_xlabel('Date')
        ax.set_ylabel('Portfolio value (USDT)')

        for _, obj in self.portfolio_objs.items():
            ax.plot(obj.portfolio_usd_value.index, obj.portfolio_usd_value.sum(axis=1), label=obj.name)

        ax.set_title('Portfolio values throughout backtesting period')
        # for tick in ax.get_xticklabels():
        #     tick.set_rotation(45)

        ax.grid(True)
        ax.legend()

        return fig

    def metrics_table(self):
        return pd.DataFrame([
            x.get_metrics() for x in self.portfolio_objs.values()
            ], index=self.portfolio_objs.keys())