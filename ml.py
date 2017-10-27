import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from scipy import interpolate
from scipy import integrate
from scipy.interpolate import InterpolatedUnivariateSpline

asda = {'names': ('rho', 'x'),
        'formats': ('f4', 'f4')}

r = np.loadtxt("/home/artem/Desktop/results/line3.txt", dtype=asda)
# r = np.loadtxt("slice_2_69.txt", dtype=asda)

from matplotlib import rc

rc('font', **{'family': 'serif', 'serif': ['Roboto']})
rc('text', usetex=True)
rc('text.latex', unicode=True)

axis_font = {'fontname': 'Arial', 'size': '18'}

fig, ax = plt.subplots()

xminorLocator = AutoMinorLocator()
yminorLocator = AutoMinorLocator()

ax.xaxis.set_minor_locator(xminorLocator)
ax.yaxis.set_minor_locator(yminorLocator)

plt.tick_params(axis='both', which='major', labelsize=18)

plt.plot(r['x'] / 1.183166e+10, np.log10(r['rho']), linewidth=2, color='black')
# plt.xlim(0.1, 1.15)
# plt.ylim(0.75, 2.7)
# plt.xticks(np.arange(0, 1.15, 0.1))

plt.title(r"$T = 0.69 P_{orb}$")

plt.xlabel(r'X ($R_{pl}$)', **axis_font)
plt.ylabel(u'Log10(Rho) ($ g/cm^3$)', **axis_font)

plt.tick_params(which='minor', length=4)
plt.tick_params(which='major', length=6)

print np.mean(r['rho']) / 1.6726231e-24, r['rho'][143] / 1.6726231e-24

# plt.plot(time, r['fx-'], time, r['fx+'])
# plt.plot(time, r['fy+'], time, r['fy-'])
# plt.plot(time, r['fx+'])

# plt.plot(time, r['fz+'], time, r['fz-'], time, r['fz+'] + r['fz-'])
# plt.plot(time, r['fx-'] + r['fy+'], time, r['fx+'] + r['fy-'])

# xmin = 0.016
# xmax = time[-1]
#
# xnew = np.arange(xmin, xmax, 0.0001)
#
# f = InterpolatedUnivariateSpline(time, mdot, k=3)
#
# plt.plot(time, mdot, xnew, f(xnew))
#
# result = f.integral(xmin, xmax)
# print '{:e}'.format(result)
plt.tight_layout()
# plt.savefig("/home/artem/Desktop/picture2.svg")
plt.show()
