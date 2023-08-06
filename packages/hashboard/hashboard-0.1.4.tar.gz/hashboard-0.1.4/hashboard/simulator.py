import numpy as np
import pandas as pd

from .history import *
from .rollouts import extract_design_matrix, Rollouts
from .parsing import parse_date, to_unix_time

from sklearn.linear_model import RidgeCV
from scipy.linalg import sqrtm


def halflives_to_alphas(halflives_in_days):

    halflives = np.maximum(1.0e-6, np.array(halflives_in_days) * 3.0)
    alphas = 1.0 - np.exp(np.log(0.5) / halflives)
    return alphas


class Simulator(object):

    def __init__(self, history=None, minphase=2520, maxphase=None, current_price=None):

        if history is None:
            history = download_history(current_price=current_price)

        self.history = history.copy()

        maxphase = maxphase or len(self.history)

        recency = np.maximum(maxphase - self.history['phase'].values, 1.0)
        weights = np.log(maxphase) - np.log(recency)
        weights[:minphase] *= 0.0
        weights[maxphase:] *= 0.0

        # truncate for technical reasons:
        self.weights = weights[1:]

        self.models = {}

    def plot_history(self, minx=None, maxx=None):

        if maxx is None:
            maxx = 48 * len(self.history)

        if minx is None:
            minx = max(0, maxx - 210000)

        from matplotlib import pyplot as plt

        if 'hashrate' not in self.models:
            self.train_hashrate_model()

        hashes_per_block = np.exp(self.history['zero_bits'] * np.log(2)).values
        block_heights = (self.history['phase'].values + 1) * 48

        df = pd.DataFrame({
            'empirical hashrate': self.history['hashrate'].values * 1.0e-18,
            'mining difficulty': hashes_per_block / 600e18,
            'price': np.nan
        }, index=block_heights)

        ax = df.loc[minx:maxx].plot(
            figsize=(12, 5),
            style=['y', 'b', 'r'],
            xlim=(minx, maxx),
            fontsize=14)

        plt.ylabel('global hashrate (EH/s)', fontsize=18)
        plt.xlabel('block height', fontsize=18)

        leg = ['empirical hashrate', 'mining difficulty', 'price', '3rd halving']
        for i in range(1, 34):
            hbh = 210000 * i
            if (minx <= hbh <= maxx):
                plt.axvline(hbh, color='grey', linestyle='--')
                ordinal_suffix = ('st' if i in [1, 21, 31] else ('nd' if i in [2, 22, 32] else ('rd' if i in [3, 23, 33] else 'th')));
                leg.append('%d%s halving' % (i, ordinal_suffix))
        plt.legend(leg, fontsize=16)

        df['price'] = self.history['price'].values
        df['price'].loc[minx:maxx].plot(ax=ax, style='r', secondary_y=True, alpha=0.4, fontsize=14)
        plt.ylabel('bitcoin price (USD)', fontsize=18)

        return ax


    def run_rollouts(self, n_rollouts, n_iters=0, until_height=None, until_time=None):

        if 'hashrate' not in self.models:
            self.train_hashrate_model()

        if 'fee' not in self.models:
            self.train_fee_model()

        laststate = {'phase': self.history['phase'].iloc[-1],
                    'features': {x : self.history[x].iloc[-1] for x in self.history.columns if x != 'phase'},
                    'design_matrices': {k : [x[-1:] for x in v['design_matrices']] for (k, v) in self.models.items()}}

        laststate['features']['last_retarget'] = self.history['start_time'].iloc[(laststate['phase'] // 42) * 42]

        r = Rollouts(laststate, n_rollouts, self.models)

        # if n_iters is specified, run that many iterations:
        for i in range(n_iters):
            r.iterate()

        # if until_height is specified, run until (at least) that height:
        if until_height is not None:
            while ((r.laststate['phase'] + 1) * 48 < until_height):
                r.iterate()

        # if until_time is specified, run until (at least) that time:
        if until_time is not None:

            until_time = to_unix_time(until_time)

            while (np.min(r.laststate['features']['end_time']) < until_time):
                r.iterate()

        return r

    def train_model(self, modelname, predictors, responses,
                    halflives=[0, 6, 24, 96, 384],
                    omegas=[1, 7],
                    model=RidgeCV, **kwargs):

        if len(halflives) > 0:
            # common usecase: autoregressive models use EWMAs of their own responses as predictors:
            predictors.append(('prev', tuple(responses), 'ewma', halflives_to_alphas(halflives)))

        if len(omegas) > 0:
            # common usecase: Fourier coefficients of time-of-week:
            predictors.append(('curr', ['start_time'], 'fourier', np.array(omegas) / (7 * 86400)))

        d = {}
        d['model'] = model(**kwargs)
        d['predictors'] = predictors
        d['responses'] = responses

        d['design_matrices'] = extract_design_matrix(predictors, self.history)

        d['X'] = np.concatenate([m.reshape((len(m), -1)) for m in d['design_matrices']], axis=1)
        d['Y'] = self.history[responses].iloc[1:].values
        d['model'].fit(d['X'], d['Y'], self.weights)

        # predictions:
        d['P'] = d['model'].predict(d['X'])

        # residuals:
        d['R'] = d['Y'] - d['P']

        # covariance matrix:
        d['cov'] = np.dot(d['R'].T, self.weights.reshape(-1, 1) * d['R']) / self.weights.sum()
        d['sqrt_cov'] = sqrtm(d['cov'])

        self.models[modelname] = d

    def train_hashrate_model(self, **kwargs):

        predictors = [('curr', ['log_reward', 'zero_bits'], 'ewma', halflives_to_alphas([0, 32]))]
        responses = ['ilhr', 'log_price']

        self.train_model('hashrate', predictors, responses, **kwargs)

        # remove unpredictable component:
        cov = self.models['hashrate']['cov']
        cov[0][0] -= (eg48_std ** 2)
        assert(np.linalg.det(cov) > 0.0)
        self.models['hashrate']['sqrt_cov'] = sqrtm(cov)

        # change prediction problem from ilhr to log_hashrate:
        self.models['hashrate']['responses'][0] = 'log_hashrate'

        # determine historical hashrate:
        epsilon_model = self.models['hashrate']['R'][:, 0]
        epsilon = np.concatenate([[0.0], epsilon_model])
        self.history['epsilon'] = epsilon
        self.history['log_hashrate'] = self.history['ilhr'] - self.history['epsilon']
        self.history['hashrate'] = np.exp(self.history['log_hashrate'])

    def train_fee_model(self, **kwargs):

        predictors = [('curr', ['epsilon'], 'ewma', halflives_to_alphas([0, 1, 4]))]
        responses = ['log_fees']

        self.train_model('fee', predictors, responses, **kwargs)
