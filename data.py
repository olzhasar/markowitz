import io
import os
import pandas as pd
import pickle
import requests

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TICKERS_FILE = os.path.join(ROOT_DIR, 'tickers.pickle')
URL = 'https://datahub.io/core/s-and-p-500-companies/r/0.csv'


def download_tickers():
    """
    Downloads csv file with tickers from remote server and pickles received
    list of tickers
    """
    with requests.get(URL, stream=True) as r:
        csv_file = io.BytesIO(r.content)
        df =  pd.read_csv(csv_file)
    tickers = df['Symbol'].tolist()
    with open(TICKERS_FILE, 'wb') as f:
        pickle.dump(tickers, f)
    return tickers


def get_tickers():
    """Reads ticker list from pickle file"""
    try:
        with open(TICKERS_FILE, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return download_tickers()


def get_tickers_dict():
    """Returns dictionary of tickers for using in dash component"""
    tickers = get_tickers()
    return [
        {'label': ticker, 'value': ticker}
        for ticker in tickers
    ]


if __name__ == '__main__':
    download_tickers()
