import pytest
from models.monte_carlo_xva import MonteCarloXVA

def test_expected_exposure_shape():
    model = MonteCarloXVA(S0=100, r=0.02, sigma=0.2, T=1, steps=12, paths=500)
    ee = model.expected_exposure()
    assert len(ee) == 13  # 12 steps + initial point

def test_cva_placeholder_positive():
    model = MonteCarloXVA(S0=100, r=0.02, sigma=0.2, T=1, steps=12, paths=500)
    cva = model.cva_placeholder()
    assert cva > 0
