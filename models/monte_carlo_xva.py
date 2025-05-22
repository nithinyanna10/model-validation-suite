import numpy as np

class MonteCarloXVA:
    def __init__(self, S0, r, sigma, T, steps, paths):
        self.S0 = S0
        self.r = r
        self.sigma = sigma
        self.T = T
        self.steps = steps
        self.paths = paths
        self.dt = T / steps

    def simulate_paths(self):
        paths = np.zeros((self.paths, self.steps + 1))
        paths[:, 0] = self.S0
        for t in range(1, self.steps + 1):
            z = np.random.standard_normal(self.paths)
            paths[:, t] = paths[:, t - 1] * np.exp((self.r - 0.5 * self.sigma ** 2) * self.dt +
                                                   self.sigma * np.sqrt(self.dt) * z)
        return paths

    def expected_exposure(self):
        paths = self.simulate_paths()
        exposures = np.maximum(paths, 0)
        return np.mean(exposures, axis=0)

    def cva_placeholder(self, lgd=0.6, credit_spread=0.01):
        EE = self.expected_exposure()
        discount_factors = np.exp(-self.r * np.linspace(0, self.T, self.steps + 1))
        cva = np.sum(credit_spread * EE * discount_factors) * self.dt * lgd
        return cva
