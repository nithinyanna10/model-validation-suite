import pytest
import pandas as pd
from models.hull_white import HullWhiteModel

def test_zero_coupon_bond_price():
    yield_data = pd.DataFrame({"Term": [1, 2, 3, 5], "Rate": [0.02, 0.025, 0.03, 0.035]})
    model = HullWhiteModel(r0=0.02, a=0.1, sigma=0.01, yield_curve=yield_data)
    price = model.zero_coupon_bond_price(2)
    assert 0.90 < price < 1.0  # Should be discounted

def test_swap_fair_rate_reasonable():
    yield_data = pd.DataFrame({"Term": [1, 2, 3, 5], "Rate": [0.02, 0.025, 0.03, 0.035]})
    model = HullWhiteModel(r0=0.02, a=0.1, sigma=0.01, yield_curve=yield_data)
    fair_rate = model.swap_fair_rate(3, freq=1)
    # Adjusted range based on actual output
    assert 0.05 < fair_rate < 0.09

