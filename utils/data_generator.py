import numpy as np
import pandas as pd
import os

def generate_vol_surface(strikes, maturities):
    vol_matrix = np.array([
        [0.20 + 0.02 * ((strike - 100)/100)**2 + 0.005 * maturity + np.random.normal(0, 0.002)
         for strike in strikes]
        for maturity in maturities
    ])
    df = pd.DataFrame(vol_matrix, index=np.round(maturities, 2), columns=np.round(strikes, 2))
    df.index.name = "Maturity"
    df.columns.name = "Strike"
    return df

def save_vol_surface(filepath="data/vol_surface.csv"):
    strikes = np.arange(50, 151, 2.5)       # 41 strike points
    maturities = np.arange(0.1, 5.1, 0.1)   # 50 maturity points
    df = generate_vol_surface(strikes, maturities)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath)

def generate_yield_curve(terms):
    base_rate = 0.015
    rates = [base_rate + 0.001 * np.log1p(term) + np.random.normal(0, 0.0005)
             for term in terms]
    df = pd.DataFrame({
        "Term": np.round(terms, 2),
        "Rate": np.round(rates, 6)
    })
    return df

def save_yield_curve(filepath="data/yield_curve.csv"):
    terms = np.linspace(0.25, 30, 120)   # 120 terms from 0.25 to 30 years
    df = generate_yield_curve(terms)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)

if __name__ == "__main__":
    save_vol_surface()
    save_yield_curve()
