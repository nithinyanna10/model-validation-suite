import numpy as np

class HullWhiteModel:
    def __init__(self, r0, a, sigma, yield_curve):
        self.r0 = r0              # Initial short rate
        self.a = a                # Mean reversion speed
        self.sigma = sigma        # Volatility
        self.yield_curve = yield_curve  # DataFrame with 'Term' and 'Rate'

    def zero_coupon_bond_price(self, T):
        # Use analytical Hull-White ZCB formula
        P0T = np.exp(-self._get_rate(T) * T)
        B = (1 - np.exp(-self.a * T)) / self.a
        A = np.exp((self.sigma ** 2 / (2 * self.a ** 2)) * (B - T + (1 - np.exp(-2 * self.a * T)) / (2 * self.a)))
        return A * P0T

    def _get_rate(self, T):
        # Linearly interpolate from yield curve
        df = self.yield_curve
        return np.interp(T, df["Term"], df["Rate"])

    def swap_fixed_leg(self, T, freq=1):
        payment_times = np.arange(freq, T + freq, freq)
        return sum([self.zero_coupon_bond_price(t) for t in payment_times]) / len(payment_times)

    def swap_fair_rate(self, T, freq=1):
        return (1 - self.zero_coupon_bond_price(T)) / self.swap_fixed_leg(T, freq)
