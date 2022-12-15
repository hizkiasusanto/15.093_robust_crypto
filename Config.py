import portfolios
from portfolios import *

DATA_FOLDER = "data"
RESULTS_FOLDER = "results"
PLOT_FILENAME = "portfolio_value_plot.png"
TABLE_FILENAME = "metrics.csv"

coins = ['BTC', 'MATIC', 'BNB', 'ETH', 'DOGE', 'ADA', 'XRP'] # coins in investment universe
rebalance_period = 'W' # 'M' for monthly, 'W' for weekly
start_date = "2022-07-01" # investment start date (previous dates will be for training)
starting_cash = 1

# List of portfolio classes except base. Do not change
port_classes = {x: globals()[x][1] for x in portfolios.__all__ if x != 'BasePortfolio'}