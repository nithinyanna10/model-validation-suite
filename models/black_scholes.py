import numpy as np
from scipy.stats import norm

class BlackScholesModel:
    def __init__(self, spot, strike, maturity, rate, volatility, option_type="call"):
        self.S = spot            # Spot price
        self.K = strike          # Strike price
        self.T = maturity        # Time to maturity (in years)
        self.r = rate            # Risk-free rate
        self.sigma = volatility  # Implied volatility
        self.option_type = option_type.lower()

    def _d1(self):
        return (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))

    def _d2(self):
        return self._d1() - self.sigma * np.sqrt(self.T)

    def price(self):
        d1 = self._d1()
        d2 = self._d2()
        if self.option_type == "call":
            return self.S * norm.cdf(d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
        elif self.option_type == "put":
            return self.K * np.exp(-self.r * self.T) * norm.cdf(-d2) - self.S * norm.cdf(-d1)
        else:
            raise ValueError("option_type must be 'call' or 'put'")

    def greeks(self):
        d1 = self._d1()
        d2 = self._d2()
        pdf_d1 = norm.pdf(d1)
        cdf_d1 = norm.cdf(d1)

        delta = norm.cdf(d1) if self.option_type == "call" else -norm.cdf(-d1)
        gamma = pdf_d1 / (self.S * self.sigma * np.sqrt(self.T))
        vega = self.S * pdf_d1 * np.sqrt(self.T)
        theta_call = (-self.S * pdf_d1 * self.sigma / (2 * np.sqrt(self.T))) - self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
        theta_put = (-self.S * pdf_d1 * self.sigma / (2 * np.sqrt(self.T))) + self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-d2)
        theta = theta_call if self.option_type == "call" else theta_put
        rho = self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(d2 if self.option_type == "call" else -d2)

        return {
            "delta": delta,
            "gamma": gamma,
            "vega": vega / 100,   # Expressed per 1% change in vol
            "theta": theta / 365, # Per day
            "rho": rho / 100      # Per 1% change in rate
        }
