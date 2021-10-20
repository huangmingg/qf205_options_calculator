from typing import Tuple
import numpy as np
import math
import pandas as pd


def calculate_price(
    closing_price: str, 
    strike_price: str, 
    interest_rate: str, 
    dividend: str, 
    maturity: str, 
    volatility: str,
    M: int,
    N: int,
    cal_type: str='explicit') -> Tuple[Tuple[float, float], str]:
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
    
    elif cal_type == 'crank':
        return __crank(S, K, r, q, T, sigma, M, N)
    
    else:
        return (None, "Calculation method not recognized")


def __explicit(
    S: float, 
    K: float, 
    r: float, 
    q: float, 
    T: float, 
    sigma: float, 
    M: int, 
    N:int) ->  Tuple[Tuple[float, float], str]:
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
        return (round(calloption[0], 2), round(putoption[0], 2)), None

    except Exception as e:
        return (None, str(e))


def __implicit(
    S: float, 
    K: float, 
    r: float, 
    q: float, 
    T: float, 
    sigma: float, 
    M: int, 
    N:int) -> Tuple[Tuple[float, float], str]:
    try:
        Smax = 2*K
        #stock step size
        deltaS=Smax/M

        #timestep size
        deltaT=T/N

        # j=np.arange(1,M,dtype=np.float)
        j=np.arange(0,M+1,1).reshape(M+1,1)
        Fc, Fp =np.maximum(j*deltaS - K , 0),np.maximum(K - j*deltaS, 0)
        #generate aj,bj and cj
        aj = [((1/2)*(deltaT)*(((r-q)*j) - (sigma ** 2) * (j ** 2))) for j in range(1,M-1+1)]
        bj = [(1 + (deltaT) * ((sigma ** 2)*(j ** 2) + r)) for j in range(1,M-1+1)]
        cj = [(-(1/2) * (deltaT) * ((sigma ** 2)*(j ** 2) + (r - q) * j)) for j in range(1,M-1+1)] 

        #generate tri diagonal matrix with 1,1 and M,M position = 1
        A = np.zeros((M+1,M+1))
        for j in range (1,M):
            A[j,j-1:j+2] = aj[j-1],bj[j-1],cj[j-1]
        A[0,0],A[M,M] = 1,1

        #generate inverse A
        Ainv = np.linalg.inv(A) 
        k = math.floor(S/deltaS)

        Call,Put = [],[]
        for i in range(N-1,-1,-1): 
            Fc[0,0],Fp[M,0] = 0,0
            Fc[M,0],Fp[0,0] = (Smax - K*(np.exp(-r*(N-i)*deltaT))), (K*(np.exp(-r*(N-i)*deltaT)))
            Fc,Fp = np.dot(Ainv,Fc),np.dot(Ainv,Fp)
            Call.insert(0, (Fc[k,0] + ((Fc[k+1,0]-Fc[k,0]) /deltaS) * (S - k * deltaS)))
            Put.insert(0, (Fp[k,0] + ((Fp[k+1,0]-Fp[k,0]) /deltaS) * (S - k * deltaS)))
        return ((round(Call[0], 2), round(Put[0], 2))), None
    
    except Exception as e:
        return (None, str(e))
    

def __crank(
    S: float, 
    K: float, 
    r: float, 
    q: float, 
    T: float, 
    sigma: float, 
    M: int, 
    N:int) -> Tuple[Tuple[float, float], str]:
    
    try:
        #Input parameters
        S = float(S) # S = Price of the underlying asset
        K = float(K) # K = strike price
        r = float(r) # r = annualised risk-free rate
        sigma = float(sigma) # σ,(sigma) = volatility 
        T = float(T) # T = time to expiration(in years)
        M = int(M) # M = space step
        N = int(N) # N = time step
        q = float(q) # q = continuous dividend yield rate


        deltaT = T/N # Δt
        Smax = 2*K 
        deltaS = Smax/M # ΔS


        def alpha_j(j):
            return 0.25 * deltaT * (sigma**2 * j**2 - (r - q) * j)

        def beta_j(j):
            return -0.5 * deltaT * (sigma**2 * j**2 + r)

        def gamma_j(j):
            return 0.25 * deltaT * (sigma**2 * j**2 + (r - q) * j)

        def discount(i):
            temp = K * np.exp(-r * (N - i) * deltaT)
            return temp

        j=np.arange(0,M+1,1).reshape(M+1,1)
        Fc, Fp =np.maximum(j*deltaS - K , 0),np.maximum(K - j*deltaS, 0)

        matrix1,matrix2   =  [np.zeros((M+1,M+1)) for k in range(2)]

        matrix1[0,0], matrix2[0,0],matrix1[M,M],matrix2[M,M]  = [1] * 4

        for j in range(1,M):
            matrix1[j,j-1:j+2]= alpha_j(j),1 + beta_j(j),gamma_j(j)
            matrix2[j,j-1:j+2]=-alpha_j(j),1 - beta_j(j), -gamma_j(j)

        k = np.int32(np.floor(S/deltaS))

        Call,Put = [],[]
        for i in range(N-1,-1,-1): 
            Fc,Fp = np.dot(matrix1,Fc),np.dot(matrix1,Fp)
            Fc[0,0],Fp[M,0] = 0,0
            Fc[M,0],Fp[0,0] = Smax - discount(i),discount(i)
            Fc,Fp = np.dot(np.linalg.inv(matrix2),Fc),np.dot(np.linalg.inv(matrix2),Fp)
            Call.insert(0, (Fc[k,0] + ((Fc[k+1,0]-Fc[k,0]) /deltaS) * (S - k * deltaS)))
            Put.insert(0, (Fp[k,0] + ((Fp[k+1,0]-Fp[k,0]) /deltaS) * (S - k * deltaS)))
        return ((round(Call[0], 2), round(Put[0], 2))), None
    except Exception as e:
        return (None, str(e))
