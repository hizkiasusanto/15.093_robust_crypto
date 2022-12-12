from utils import *
from Config import *

if __name__ == "__main__":
    df = generate_data_df(coins)

    portfolio_instances = {}

    for port_name, portfolio in port_classes.items():
        portfolio_instances[port_name] = portfolio(coins, df, start_date, rebalance_period)
        portfolio_instances[port_name].backtest(starting_cash=starting_cash)

    