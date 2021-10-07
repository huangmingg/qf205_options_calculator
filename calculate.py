from typing import Tuple
import numpy as np
import math
import pandas as pd
from scipy.stats import norm


def calculate_price(
    closing_price: str, 
    strike_price: str, 
    interest_rate: str, 
    dividend: str, 
    maturity: str, 
    volatility: str,
    M: int,
    N: int,
    cal_type: str='explicit') -> Tuple[float, float]:
    S = float(closing_price)
    K = float(strike_price)
    r = float(interest_rate) / 100
    sigma = float(volatility) / 100
    q = float(dividend) / 100
    T = int(maturity) / 365
    M = int(M)
    N = int(N)

    if cal_type == 'explicit':
        return __explicit(S, K, r, q, T, sigma, M, N)

    elif cal_type == 'implicit':
        return __implicit(S, K, r, q, T, sigma, M, N)
    else:
        print("Calculation method not recognized") 
        return (0,0)


def __explicit(
    S: float, 
    K: float, 
    r: float, 
    q: float, 
    T: float, 
    sigma: float, 
    M: int, 
    N:int) -> Tuple[float, float]:
    """ 
    Using Black-Scholes formula to calculate option price
    returns a tuple with 2 elements (call option, put option)
    input S can be stock price or stock symbol 
    """
    try:
        ## TODO: Cleanup
        S = float(S) # S = Price of the underlying asset
        K = float(K) # K = strike price
        r = float(r) # r = annualised risk-free rate
        sigma = float(sigma) # σ,(sigma) = volatility 
        T = float(T) # T = time to expiration(in years)
        M = int(M) # M = space step
        N = int(N) # N = time step
        q = float(q) # q = continuous dividend yield rate

        d1 = (math.log(S/K) + (r - q + sigma**2/2)*T) / (sigma * T**0.5)
        d2 = d1 - sigma*T**0.5
        c = S * math.e**(-q*T) * norm.cdf(d1) - K * math.e**(-r*T) * norm.cdf(d2)
        p = K * math.e**(-r*T) * norm.cdf(-d2) - S * math.e**(-q*T) * norm.cdf(-d1)
        return c, p

    except Exception as e:
        print(e)
        return (0,0)


def __implicit(
    S: float, 
    K: float, 
    r: float, 
    q: float, 
    T: float, 
    sigma: float, 
    M: int, 
    N:int) -> Tuple[float, float]:
    pass
