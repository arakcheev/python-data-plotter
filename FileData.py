__author__ = 'artem'

import numpy as np
import math
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import Parameters
import Utils
from matplotlib.colors import LogNorm
from spacepy.pybats import bats

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


class FileData(bats.Bats2d):
    def __init__(self, filename):

        bats.Bats2d.__init__(self, filename)

        self['log_rho'] = np.log(self['rho'])
        self['T'] = np.log10((10e7 / 1.3806) * (self['p'] / (self['rho'])))
        self['x'] -= 73.6

    def plotContour(self, axes):

        rho_min = self['log_rho'].min()
        rho_max = self['log_rho'].max()

        levels = np.arange(rho_min, rho_max, 0.07)

        axes.contour(self['x'], self['y'], self['log_rho'], levels)

    def plotPressure(self, axes):

        p_min = math.log(self['p'].min())
        p_max = math.log(self['p'].max())

        levels = np.arange(p_min, p_max, 0.005)

        axes.contour(self['x'], self['y'], np.log(self['p']), levels)
        
    def plotVelocityFiled(self, axes):
        _levels = 50

        # Build new linspace
        x = np.linspace(self['x'].min(), self['x'].max(), _levels)
        # x = np.linspace(73, 73.5, _levels)
        y = np.linspace(self['y'].min(), self['y'].max(), _levels)
        # y = np.linspace(-3, -2, _levels)

        v_x = np.zeros((_levels, _levels))
        v_y = np.zeros((_levels, _levels))

        for i in range(0, self['grid'][0], 15):
            for j in range(0, self['grid'][1], 15):
                _v = self['ux'][i, j]
                _u = self['uy'][i, j]
                for k in range(0, _levels - 1):
                    for n in range(0, _levels - 1):

                        if x[k + 1] >= self['x'][i] >= x[k] and y[n + 1] >= self['y'][j] >= y[n]:
                            v_x[k, n] = _v
                            v_y[k, n] = _u

        axes.quiver(x, y, v_x, v_y, units="xy", scale=70, width=0.05)

    def plotRocheLobe(self, axes):
        _roche = np.zeros((self['grid'][0], self['grid'][1]))

        for j in range(0, self['grid'][1]):
            for i in range(0, self['grid'][0]):
                _roche[j, i] = Utils.roche((self['x'][i] + 73.6) * params.planet_radius,
                                           self['y'][j] * params.planet_radius, 0)

        # One equipotential level for piloting lobe where platen in
        roc0 = Utils.roche(params.ab - 0.547 * params.sunRadius, 0.0, 0.0)

        roche_levels = [roc0]

        axes.contour(self['x'], self['y'], _roche, roche_levels, colors="r", linewidths=[2])

    def srez_y(self, var, y, axes, initial_data=None, y_limit=None, label="", *args, **kwargs):

        if var in ['x', 'y', 'grid']:
            raise KeyError('Invalid key for srez')

        ind = findCloasestIndex(self['y'], y)

        plot = np.zeros(self['grid'][0])

        if initial_data is not None:
            for i in range(0, self['grid'][0]):
                if var is "T":
                    plot[i] = self[var][i, ind] / initial_data[var][i, ind]
                else:
                    plot[i] = (self[var][i, ind] - initial_data[var][i, ind]) / initial_data[var][i, ind]
                    # math.log(self['p'][i, ind] / self['rho'][i, ind])   #
                    # plot[i] = self[var][i, ind]  # math.log(self['p'][i, ind] / self['rho'][i, ind])   #
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


        # ind = self.ny / 2
        # for j in range(0, self.ny):
        #     if math.fabs(self.y[j]) < 0.1:
        #         ind = j
        #
        # f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col')
        #
        # self.plotContour(ax1)
        # self.plotRocheLobe(ax1)
        # ax1.set_title("Contour rho")
        # ax1.set_xlabel(r'Rpl')
        # ax1.set_ylabel(r'Rpl')
        # ax1.set_xticks([40, 68.6, 78.6, 100])
        # ax1.grid(which='both')
        #
        # _ux = self.U[ind, :]
        # ax3.plot(self.x, _ux)
        # ax3.set_title("Ux")
        # ax3.set_ylabel(r'V (km/s)')
        # ax3.set_ylim([-60, 160])
        # ax3.set_xticks([40, 68.6, 78.6, 100])
        # ax3.grid(which='both')
        #
        # _logrho = self.logRho[ind, :]
        # ax2.plot(self.x, _logrho)
        # ax2.set_title("log(rho) ")
        # ax2.set_ylabel(r'log rho')
        # ax2.set_xlabel(r'Rpl')
        # ax2.set_ylim([_logrho.min() - 2, _logrho.max() + 2])
        # ax2.set_xticks([40, 68.6, 78.6, 100])
        # ax2.grid(which='both')
        #
        # ax4.plot(self.x, self.p[ind, :])
        # ax4.set_title("px")
        # ax4.set_xticks([40, 68.6, 78.6, 100])
        # ax4.grid(which='both')
        # # ax4.set_ylabel(r'U (km/s)')
        # ax4.set_ylim([0, 30])
        #
        # return f

    def moment_contour(self, axes, initial_data):

        moment = np.zeros(self['grid'])

        for i in range(1, self['grid'][0] - 1):
            for j in range(1, self['grid'][1] - 1):
                dx = (self['x'][i] + self['x'][i + 1]) / 2
                dy = (self['y'][i] + self['y'][i + 1]) / 2

                ds = dx * dy

                moment[i, j] = \
                    self['rho'][i, j] * (self['ux'][i, j] + self['uy'][i, j]) * ds \
                    - initial_data['rho'][i, j] * (initial_data['ux'][i, j] + initial_data['uy'][i, j]) * ds

        _min = moment.min()
        _max = moment.max()

        levels = np.linspace(_min, _max, 1000)

        cmap = plt.get_cmap('PiYG')

        return axes.pcolormesh(self['x'], self['y'], moment, vmin=-1e10, vmax=1e10)

    def add_body(self, ax=None, facecolor='lightgrey', DoPlanet=True, ang=0.0, **extra_kwargs):
        from matplotlib.patches import Ellipse

        dbody = 2.15 * 3  # self.attrs['rbody']
        body = Ellipse((0, 0), dbody, dbody, facecolor='lightgrey', zorder=999)
        ax.add_artist(body)
