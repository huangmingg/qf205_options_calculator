from typing import List, Tuple
from datetime import date
import pandas as pd
import requests


def get_tickers() -> Tuple[List[str], str]:
    try:
        return list(pd.read_csv('stock_list.csv').Symbol), ''
    except Exception as e:
        return None, str(e)


def get_closing_price(ticker: str) -> Tuple[float, str]:
    try:
        res = requests.get(f'https://finance.yahoo.com/quote/{ticker}?p={ticker}')
        closing_price = pd.read_html(res.text, index_col=0)[0].loc['Previous Close', 1]
        return (round(float(closing_price), 2), '')
    except Exception as e:
        return None, f'Data for {ticker} not found, please key in the closing price manually'