from spacepy.pybats import PbData
import math
import numpy as np

__author__ = 'artem'
import Parameters
import Utils

params = Parameters.Parameters


def findCloasestIndex(array, value):
    # import math

    # low = 0
    # high = array.__len__() - 1
    #
    # while low < high:
    #     mid = (low + high) / 2
    #     d1 = math.fabs(array[mid] - value)
    #     d2 = math.fabs(array[mid + 1] - value)
    #     if (d2 <= d1):
    #         low = mid + 1
    #     else:
    #         high = mid

    idx = (np.abs(array - value)).argmin()

    return idx


class Model(PbData):
    def __init__(self, *args, **kwargs):
        super(PbData, self).__init__(*args, **kwargs)

    def plot_contour(self, axes):

        rho_min = self['log_rho'].min()
        rho_max = self['log_rho'].max()

        levels = np.arange(rho_min, rho_max, 0.05)

        axes.contour(self['x'], self['y'], self['log_rho'], levels)

    def plot_velocity_filed(self, axes):
        _levels = 50
        # How often arrows 
        _freq = 15

        # Build new linspace
        x = np.linspace(self['x'].min(), self['x'].max(), _levels)
        y = np.linspace(self['y'].min(), self['y'].max(), _levels)

        v_x = np.zeros((_levels, _levels))
        v_y = np.zeros((_levels, _levels))

        for j in range(0, self['grid'].attrs['ny'], _freq):
            for i in range(0, self['grid'].attrs['nx'], _freq):
                _v = self['vx'][j, i]
                _u = self['vy'][j, i]
                for n in range(0, _levels - 1):
                    for k in range(0, _levels - 1):
                        if x[k + 1] >= self['x'][i] >= x[k] and y[n + 1] >= self['y'][j] >= y[n]:
                            v_x[k, n] = _v
                            v_y[k, n] = _u
        axes.quiver(x, y, v_x, v_y, scale=30, width=0.002)

    def plot_roche_lobe(self, axes):
        _roche = np.zeros(self['rho'].shape)

        for j in range(0, self['grid'].attrs['ny']):
            for i in range(0, self['grid'].attrs['nx']):
                _roche[j, i] = Utils.roche((self['x'][i] + 73.6) * params.planet_radius,
                                           self['y'][j] * params.planet_radius, 0)

                # One equipotential level for piloting lobe where platen in
        roc0 = Utils.roche(params.ab - 0.547 * params.sunRadius, 0.0, 0.0)

        roche_levels = [roc0]

        axes.contour(self['x'], self['y'], _roche, roche_levels, colors="r", linewidths=[2])
