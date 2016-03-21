from Model import Model

__author__ = 'artem'

import numpy as np
import matplotlib.pyplot as plt
from spacepy.pybats import bats
from Parameters import Parameters


class FileData(bats.Bats2d, Model):
    def sub_title(self):
        return ' time = ' + "{:.2}".format(self.attrs['time'] / Parameters.period) + " "

    def get_name(self):
        return str(self.attrs['iter'])

    def __init__(self, filename, *args, **kwargs):
        # super(bats.Bats2d, self).__init__(self, filename, *args, **kwargs)
        # super(FileData, self).__init__(*args, **kwargs)

        super(FileData, self).__init__(filename)

        self['log_rho'] = np.log(self['rho'])
        self['T'] = np.log10((10e7 / 1.3806) * (self['p'] / (self['rho'])))
        self['x'] -= 98.13
        self['grid'].attrs['nx'] = self['grid'][0]
        self['grid'].attrs['ny'] = self['grid'][1]

        self['vx'] = self['ux']
        self['vy'] = self['uy']

        iter = [key for key in self.keys() if key not in ['grid', 'x', 'y']]

        # for key in iter:
        #     self[key] = self[key].T

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
