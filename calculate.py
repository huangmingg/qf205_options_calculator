import numpy as np
import math
import requests
import pandas as pd

def explicit(S, K, r, q, T, sigma, M, N):
    """ 
    Using Black-Scholes formula to calculate option price
    returns a tuple with 4 elements (call option, put option, is_error (boolean), error message)
    input S can be stock price or stock symbol 
    """
    try:
        if isinstance(S, float) or isinstance(S, int):
            S = float(S) # S = Price of the underlying asset
        elif isinstance(S, str):
            res = requests.get(f'https://finance.yahoo.com/quote/{S}?p={S}')
            closing_price = pd.read_html(res.text, index_col=0)[0].loc['Previous Close', 1]
            S = float(closing_price) # S = Price of the underlying asset
        K = float(K) # K = strike price
        r = float(r) # r = annualised risk-free rate
        sigma = float(sigma) # σ,(sigma) = volatility 
        T = float(T) # T = time to expiration(in years)
        M = int(M) # M = space step
        N = int(N) # N = time step
        q = float(q) # q = continuous dividend yield rate

        Smax = 2*K
        deltaS = Smax/M #stockstep size 
        deltaT = T/N #timestep size

        # j = np.arange(1,M,dtype=np.float)

        aj = [(1/2)*(deltaT)*(sigma**2*j**2-(r-q)*j) for j in range(1,M-1+1)]
        bj = [1-(deltaT)*(sigma**2*j**2+r) for j in range(1,M-1+1)]
        cj = [(1/2)*(deltaT)*(sigma**2*j**2+(r-q)*j) for j in range(1,M-1+1)]

        j=np.arange(0,M+1,1).reshape(M+1,1)
        fnjcall, fnjput = np.maximum(j*deltaS - K, 0), np.maximum(K - j*deltaS, 0) #2 

        matrixA = np.zeros((M+1,M+1))
        matrixA[0,0], matrixA[M,M] = 1, 1
        for j in range(1,M):
            matrixA[j,j-1:j+2] = aj[j-1], bj[j-1], cj[j-1]

        k = math.floor(S/deltaS)
        calloption, putoption = [], []

        for i in range(N-1,-1,-1):
            fnjcall, fnjput = np.dot(matrixA, fnjcall), np.dot(matrixA,fnjput)
            fnjcall[0,0],fnjput[M,0] = 0,0 
            fnjcall[M,0],fnjput[0,0] = (Smax - (K*np.exp(-r*(N-i)*deltaT)), (K*np.exp(-r*(N-i)*deltaT)))
            calloption.insert(0,fnjcall[k,0] + ((fnjcall[k+1, 0]-fnjcall[k,0]) /deltaS) * (S - k * deltaS))
            putoption.insert(0,fnjput[k,0] + ((fnjput[k+1, 0]-fnjput[k,0]) /deltaS) * (S - k * deltaS))
        return (calloption[0],putoption[0],False,None)
    except Exception as e:
        return ('ERROR','ERROR', True, e)
