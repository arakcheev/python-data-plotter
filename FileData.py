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
    import math

    low = 0
    high = array.__len__() - 1

    while low < high:
        mid = (low + high) / 2
        d1 = math.fabs(array[mid] - value)
        d2 = math.fabs(array[mid + 1] - value)
        if (d2 <= d1):
            low = mid + 1
        else:
            high = mid

    return high


class FileData(bats.Bats2d):
    def __init__(self, filename):

        bats.Bats2d.__init__(self, filename)

        log_rho = np.zeros(self['grid'])

        for i in range(0, self['grid'][0]):
            for j in range(0, self['grid'][1]):
                log_rho[i, j] = math.log(self['rho'][i, j])

        self['log_rho'] = log_rho

    def plotContour(self, axes):

        rho_min = math.log(self['rho'].min())
        rho_max = math.log(self['rho'].max())

        levels = np.arange(rho_min, rho_max, 0.05)

        axes.contour(self['x'], self['y'], self['log_rho'], levels)

    def plotVelocityFiled(self, axes):
        _levels = 50

        # Build new linspace
        # x = np.linspace(self['x'].min(), self['x'].max(), _levels)
        x = np.linspace(73, 73.5, _levels)
        # y = np.linspace(self['y'].min(), self['y'].max(), _levels)
        y = np.linspace(-3, -2, _levels)

        v_x = np.zeros((_levels, _levels))
        v_y = np.zeros((_levels, _levels))

        for i in range(0, self['grid'][0], 5):
            for j in range(0, self['grid'][1], 5):
                _v = self['ux'][i, j]
                _u = self['uy'][i, j]
                for k in range(0, _levels - 1):
                    for n in range(0, _levels - 1):

                        if x[k + 1] >= self['x'][i] >= x[k] and y[n + 1] >= self['y'][j] >= y[n]:
                            v_x[k, n] = _v
                            v_y[k, n] = _u

        axes.quiver(x, y, v_x, v_y, v_x, cmap=cm.seismic)

    def plotRocheLobe(self, axes):
        _roche = np.zeros((self['grid'][0], self['grid'][1]))

        for j in range(0, self['grid'][1]):
            for i in range(0, self['grid'][0]):
                _roche[j, i] = Utils.roche(self['x'][i] * params.planet_radius,
                                           self['y'][j] * params.planet_radius, 0)

        # One equipotential level for piloting lobe where platen in
        roc0 = Utils.roche(params.ab - 0.547 * params.sunRadius, 0.0, 0.0)

        roche_levels = [roc0]

        axes.contour(self['x'], self['y'], _roche, roche_levels, colors="r", linewidths=[2])

    def srez_y(self, var, y, axes, initial_data=None, y_limit=None, *args, **kwargs):

        if var in ['x', 'y', 'grid']:
            raise KeyError('Invalid key for srez')

        ind = findCloasestIndex(self['y'], y)

        if y > 0:
            ind = 230

        plot = self[var][:, ind]

        if initial_data is not None:

            for i in range(0, self['grid'][0]):
                plot[i] = (self[var][i, ind] - initial_data[var][i, ind])  # / initial_data[var][i, ind]

        axes.plot(self['x'], plot, *args)

        # print "{:.2E}".format(diff.max()), "{:.2E}".format(diff.min())
        # print "{:.2E}".format(self[var][:,ind].max()), "{:.2E}".format(self[var][:,ind].min())
        # print "{:.2E}".format(initial_data[var][:,ind].max()), "{:.2E}".format(initial_data[var][:,ind].min())


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
        axes.axis([self['x'].min(), self['x'].max(), y_min, y_max])

        # axes.plot((69.6, 69.6), (y_min, y_max), 'r--')
        # axes.plot((73.60, 73.60), (y_min, y_max), 'g--')
        # axes.plot((73.60 - 2.5 - 0.03, 73.60 - 2.5 - 0.03), (y_min, y_max), 'b--')
        # axes.plot((73.60 + 2.5, 73.60 + 2.5), (y_min, y_max), 'b--')

        return axes


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
                    self['rho'][i, j] * (self['ux'][i, j]) * ds \
                    - initial_data['rho'][i, j] * initial_data['ux'][i, j] * ds

        _min = moment.min()
        _max = moment.max()

        levels = np.linspace(_min, _max, 1000)

        cmap = plt.get_cmap('PiYG')

        return axes.pcolormesh(self['x'], self['y'], moment, vmin=-1e10, vmax=1e10)

    def srezContourVx(self, ySrezLevel=0.2):
        ind = findCloasestIndex(self.y, ySrezLevel)

        # for j in range(0, self.ny):
        #     if math.fabs(self.y[j]) < 0.1:
        #         ind = j

        srezLevel = self.y[ind]

        import matplotlib.gridspec as gridspec

        gs1 = gridspec.GridSpec(2, 1, height_ratios=[2, 1])

        f = plt.figure(figsize=[17, 12.8])

        ax1 = plt.subplot(gs1[0])

        ax2 = plt.subplot(gs1[1])

        # f, (ax1, ax2) = plt.subplots(2)

        ticks = [40, 68.6, 78.6, 100]
        axes = [self.x.min(), self.x.max(), self.y.min(), self.y.max()]

        self.plotContour(ax1)
        self.plotRocheLobe(ax1)

        ax1.set_title("Contour rho")
        ax1.set_xlabel(r'Rpl')
        ax1.set_ylabel(r'Rpl')
        ax1.set_xticks(ticks)
        ax1.axis(axes)
        ax1.set_autoscale_on(False)
        ax1.grid(which='both')

        ax1.plot((self.x.min(), self.x.max()), (srezLevel, srezLevel), '--')

        ax1.plot((69.6, 69.6), (self.y.min(), self.y.max()), 'r--')

        # ax1.plot(self.x, [srezLevel for x in range(0, self.ny)], '--')

        _ux = self.U[ind, :]
        ax2.plot(self.x, _ux)
        ax2.set_title("Ux")
        ax2.set_ylabel(r'V (km/s)')
        ax2.set_ylim([-60, 160])
        ax2.set_xticks(ticks)
        ax2.axis([self.x.min(), self.x.max(), -60, 160])
        ax2.set_autoscale_on(False)
        ax2.grid(which='both')

        ax2.plot((69.6, 69.6), (-60, 160), 'r--')

        return f
