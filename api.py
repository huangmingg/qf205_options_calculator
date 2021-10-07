from typing import List
from datetime import date


def get_tickers() -> List[str]:
    return ['AAPL', 'GOOG']


def get_closing_price(ticker: str, selected_date: date) -> float:
    pass