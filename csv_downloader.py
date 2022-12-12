from itertools import combinations
import requests, zipfile
from io import BytesIO
from tqdm import tqdm
import os

from Config import DATA_FOLDER

def make_pair(coin1, coin2):
    '''
    Returns the pair symbol
    e.g., 'BTC' and 'ETH' -> 'BTCETH'
    '''
    return f'{coin1}{coin2}'

def get_url(pair, month, freq = '1h'):
    '''
    Returns the URL of K-line data given crypto pair, month and frequency
    '''
    return ('https://data.binance.vision/data/spot/monthly/klines/'
            f'{pair}/{freq}/{pair}-{freq}-{month}.zip')

def download_csv(url, DATA_FOLDER=DATA_FOLDER):
    '''
    Downloads CSV file to working directory if URL is valid, returns the file name of saved file.
    Else raises ValueError
    '''
    r = requests.get(url, stream=True)
    
    if r.status_code == 200:
        z = zipfile.ZipFile(BytesIO(r.content))
        extracted = z.namelist()
        z.extractall(DATA_FOLDER)
        z.close()
        return
    
    else:
        raise ValueError(f"Error {r.status_code}: URL not found")

# Top 10 pairs by total market cap (https://www.binance.com/en/altcoins/trending)
cryptos = ['BTC', 'ETH', 'USDT', 'BNB', 'USDC', 'BUSD', 'XRP', 'DOGE', 'ADA', 'MATIC']
pair_tuples = list(combinations(cryptos, 2)) # Make tuples of every pair

months = [f'2022-0{x}' for x in range(6, 10)] # June to Sep 2022

if __name__ == "__main__":
    download_count = 0
    pairs_not_found = []

    for pair in tqdm(pair_tuples):
        pair_found = None
        
        # Try first pair. E.g., "BTC" and "ETH" -> "BTCETH"
        first_pair = make_pair(*pair)
        
        url = get_url(first_pair, months[0])
        
        try:
            download_csv(url)
            download_count += 1
            pair_found = first_pair
            
        except ValueError:
            pass
            
        # If first pair not found, try second pair. E.g., "BTC" and "ETH" -> "ETHBTC"
        if not pair_found:
            second_pair = make_pair(*pair[::-1])
            url = get_url(second_pair, months[0])
            try:
                download_csv(url)
                download_count += 1
                pair_found = second_pair
            
            except ValueError:
                pass
            
        # If neither is found, append to pairs not found
        if not pair_found:
            pairs_not_found.append(pair)
            
        # Else, download subsequent months
        else:
            for month in months[1:]:
                url = get_url(pair_found, month)
                
                download_csv(url)
                download_count += 1

    print(f"Downloaded {download_count} CSV files onto {os.getcwd()}");print()
    print("Pairs not found:")
    for pair in pairs_not_found:
        print(pair)
