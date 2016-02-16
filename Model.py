from spacepy.pybats import PbData
import math
import numpy as np

__author__ = 'artem'
import Parameters
import Utils

params = Parameters.Parameters


def findCloasestIndex(array, value):
    return (np.abs(array - value)).argmin()


class Model(PbData):
    def __init__(self, *args, **kwargs):
        super(PbData, self).__init__(*args, **kwargs)

    def plot_contour(self, axes, _item_config):
        var = _item_config['var']
        var_legend = _item_config['var_legend']

        levels_step = _item_config['levels_step']

        var_min = self[var].min()
        var_max = self[var].max()

        levels = np.arange(var_min, var_max, levels_step)

        axes.contour(self['x'], self['y'], self[var], levels)

        axes.set_ylabel(var_legend)
        axes.set_xlabel(r"R_{pl}")

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

    def plot_roche_lobe(self, axes, _item_config):
        _roche = np.zeros(self['rho'].shape)

        for j in range(0, self['grid'].attrs['ny']):
            for i in range(0, self['grid'].attrs['nx']):
                _roche[j, i] = Utils.roche((self['x'][i] + 73.6) * params.planet_radius,
                                           self['y'][j] * params.planet_radius, 0)

        # One equipotential level for piloting lobe where platen in
        roc0 = Utils.roche(params.ab - 0.547 * params.sunRadius, 0.0, 0.0)

        roche_levels = [roc0]

        axes.contour(self['x'], self['y'], _roche, roche_levels, colors="r", linewidths=[2])

    def slice_y(self, var, y, axes, initial_data=None, y_limit=None, label="", *args, **kwargs):

        if var in ['x', 'y', 'grid']:
            raise KeyError('Invalid key for slice')

        ind = findCloasestIndex(self['y'], y)

        plot = np.zeros(self['grid'].attrs['ny'])

        if initial_data is not None:
            for i in range(0, self['grid'].attrs['nx']):
                if var is "T":
                    plot[i] = self[var][ind, i] / initial_data[var][ind, i]
                else:
                    plot[i] = (self[var][ind, i] - initial_data[var][ind, i]) / initial_data[var][ind, i]
        else:
            plot = self[var][ind, :]

        axes.plot(self['x'], plot, label=label, *args, **kwargs)

        # axes.axhline(50, self['x'].min(), self['x'].max(), linewidth=4, color='r')

        if y_limit is not None:
            y_max = y_limit[1]
        else:
            y_max = plot.max()

        if y_limit is not None:
            y_min = y_limit[0]
        else:
            y_min = plot.min()

        # axes.set_xlabel(r'Rpl')
        # axes.set_ylabel(r' $(\rho - \rho_{init})/\rho_{init}$ ')
        axes.set_ylim([y_min, y_max])

        # axes.plot((69.6, 69.6), (y_min, y_max), 'r--')
        # axes.plot((73.60, 73.60), (y_min, y_max), 'g--')
        # axes.plot((73.60 - 2.5 - 0.03, 73.60 - 2.5 - 0.03), (y_min, y_max), 'b--')
        # axes.plot((73.60 + 2.5, 73.60 + 2.5), (y_min, y_max), 'b--')

        return (axes, self['y'][ind])

    def get_name(self):
        raise NotImplementedError("Please Implement this method")

    def sub_title(self):
        raise NotImplementedError("Please Implement this method")
