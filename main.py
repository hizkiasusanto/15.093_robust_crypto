from utils import *
from Config import *
from Evaluator import Evaluator

if __name__ == "__main__":
    df = generate_data_df(coins)

    portfolio_instances = {}

    for port_name, portfolio in port_classes.items():
        portfolio_instances[port_name] = portfolio(coins, df, start_date, rebalance_period)
        portfolio_instances[port_name].backtest(starting_cash=starting_cash)

    evaluator = Evaluator(portfolio_instances)

    fig = evaluator.plot()

    fig.savefig(f"{RESULTS_FOLDER}/{PLOT_FILENAME}")
    print(f"Plot figure saved as {RESULTS_FOLDER}/{PLOT_FILENAME}")

    metrics_df = evaluator.metrics_table()

    metrics_df.to_csv(f"{RESULTS_FOLDER}/{TABLE_FILENAME}")
    print(f"Metrics saved as {RESULTS_FOLDER}/{TABLE_FILENAME}")