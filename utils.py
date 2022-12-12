from glob import glob
import pandas as pd
from datetime import datetime

from Config import DATA_FOLDER

def get_usdt_pair(coin, DATA_FOLDER = DATA_FOLDER):
    files = sorted(glob(f"{DATA_FOLDER}/{coin}USDT-1h-*.csv"))
    
    df = pd.DataFrame(columns = ["Close time","Close"])
    for file in files:
        temp = pd.read_csv(file, header=None)
        temp.columns = ["Open time", "Open", "High", "Low", 
                        "Close", "Volume", "Close time", "Quote asset volume",
                        "Number of trades", "Taker buy base asset volume",
                        "Taker buy quote asset volume", "Ignore"]
        
        df = pd.concat([df, temp[["Close time", "Close"]]])
    df['Close time'] = df['Close time'].apply(lambda x: datetime.fromtimestamp((x+10800001)/1000))
    
    df.set_index('Close time', inplace=True)
    df.columns = [f"{coin}USDT"]
    
    return df

def generate_data_df(coins, DATA_FOLDER=DATA_FOLDER):
    df = pd.DataFrame()
    for coin in coins:
        temp = get_usdt_pair(coin, DATA_FOLDER)
        
        df = pd.concat([df, temp], axis=1)
        
    return df