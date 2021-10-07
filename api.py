from typing import List
from datetime import date
import pandas as pd
import requests


def get_tickers() -> List[str]:
    return list(pd.read_csv('stock_list.csv').Symbol)


def get_closing_price(ticker: str) -> float:
    try:
        res = requests.get(f'https://finance.yahoo.com/quote/{ticker}?p={ticker}')
        closing_price = pd.read_html(res.text, index_col=0)[0].loc['Previous Close', 1]
        return float(closing_price)
    except Exception as e:
        print(e)
        return 0
