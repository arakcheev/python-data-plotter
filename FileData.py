__author__ = 'artem'

import numpy
import math
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import Parameters
import Utils

params = Parameters.Parameters


class FileData:
    def __init__(self, filename):
        f = open(filename, 'r')

        # Read and ignore header lines
        header1 = f.readline()  # Units
        header2 = f.readline().strip().split()
        header3 = f.readline().strip().split()
        header4 = f.readline()
        header5 = f.readline()

        self.fileNumber = int(header2[0])
        self.time = float(header2[1])

        self.nx = int(header3[0])
        self.ny = int(header3[1])

        # print self.nx, self.ny

        self.x = numpy.zeros(self.nx)
        self.y = numpy.zeros(self.ny)
        self.rho = numpy.zeros((self.nx, self.ny))
        self.logRho = numpy.zeros((self.nx, self.ny))
        self.p = numpy.zeros((self.nx, self.ny))
        self.U = numpy.zeros((self.nx, self.ny))
        self.V = numpy.zeros((self.nx, self.ny))

        # for j in range(0, self.ny):
        #     for i in range(0, self.ny):
        #         line = f.readline().strip()

        line = ""

        for j in range(0, self.ny):
            for i in range(0, self.nx):
                line = f.readline().strip()
                columns = line.split()

                _x = float(columns[0])
                _y = float(columns[1])
                _rho = float(columns[2])
                _vx = float(columns[3])
                _vy = float(columns[4])
                _p = float(columns[9])

                self.x[i] = _x
                self.y[j] = _y

                self.U[j, i] = _vx
                self.V[j, i] = _vy

                self.rho[j, i] = _rho
                self.logRho[j, i] = math.log(_rho)
                self.p[j, i] = math.log(_p)
        f.close()

    def plotContour(self, axes):

        rho_min = self.logRho.min()
        rho_max = self.logRho.max()

        levels = numpy.arange(rho_min, rho_max, 0.1)

        axes.contour(self.x, self.y, self.logRho, levels)

    def plotVelocityFiled(self, axes):
        _levels = 30

        x = numpy.linspace(self.x.min(), self.x.max(), _levels)
        y = numpy.linspace(self.y.min(), self.y.max(), _levels)

        v_x = numpy.zeros((_levels, _levels))
        v_y = numpy.zeros((_levels, _levels))

        for j in range(0, self.nx, 5):
            for i in range(0, self.ny, 5):
                _v = -self.V[j, i]
                _u = -self.U[j, i]
                for k in range(0, _levels - 1):
                    for n in range(0, _levels - 1):

                        if x[k + 1] >= self.x[i] >= x[k] and y[n + 1] >= self.y[j] >= y[n]:
                            v_x[k, n] = _v
                            v_y[k, n] = _u

        axes.quiver(x, y, v_x, v_y, v_x, cmap=cm.seismic, headlength=5)

    def plotRocheLobe(self, axes):
        _roche = numpy.zeros((self.nx, self.ny))

        for j in range(0, self.ny):
            for i in range(0, self.nx):
                _roche[j, i] = Utils.roche(self.x[i] * params.planetRadius, self.y[j] * params.planetRadius, 0)

        # One equipotential level for piloting lobe where platen in
        roc0 = Utils.roche(params.ab - 0.547 * params.sunRadius, 0.0, 0.0)

        rochelevels = [roc0]

        axes.contour(self.x, self.y, _roche, rochelevels, colors="r", linewidths=[2])

    def srez(self):
        ind = self.ny / 2
        for j in range(0, self.ny):
            if math.fabs(self.y[j]) < 0.1:
                ind = j

        f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col')

        self.plotContour(ax1)
        ax1.set_title("Contour rho")
        ax1.set_xlabel(r'Rpl')
        ax1.set_ylabel(r'Rpl')
        ax1.set_xticks([40, 68.6, 78.6, 100])
        ax1.grid(which='both')

        _ux = self.U[ind, :]
        ax3.plot(self.x, _ux)
        ax3.set_title("Ux")
        ax3.set_ylabel(r'V (km/s)')
        ax3.set_ylim([-60, 160])
        ax3.set_xticks([40, 68.6, 78.6, 100])
        ax3.grid(which='both')

        _logrho = self.logRho[ind, :]
        ax2.plot(self.x, _logrho)
        ax2.set_title("log(rho) ")
        ax2.set_ylabel(r'log rho')
        ax2.set_xlabel(r'Rpl')
        ax2.set_ylim([_logrho.min() - 2, _logrho.max() + 2])
        ax2.set_xticks([40, 68.6, 78.6, 100])
        ax2.grid(which='both')

        ax4.plot(self.x, self.p[ind, :])
        ax4.set_title("px")
        ax4.set_xticks([40, 68.6, 78.6, 100])
        ax4.grid(which='both')
        # ax4.set_ylabel(r'U (km/s)')
        ax4.set_ylim([0, 30])

        return f
