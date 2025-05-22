import pytest
from models.black_scholes import BlackScholesModel
import numpy as np

def test_call_option_price():
    model = BlackScholesModel(spot=100, strike=100, maturity=1, rate=0.05, volatility=0.2, option_type="call")
    price = model.price()
    assert np.isclose(price, 10.45, atol=0.5)

def test_put_option_price():
    model = BlackScholesModel(spot=100, strike=100, maturity=1, rate=0.05, volatility=0.2, option_type="put")
    price = model.price()
    assert np.isclose(price, 5.57, atol=0.5)

def test_greeks_structure():
    model = BlackScholesModel(100, 100, 1, 0.05, 0.2)
    greeks = model.greeks()
    assert all(g in greeks for g in ["delta", "gamma", "vega", "theta", "rho"])
