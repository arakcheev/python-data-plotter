import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from matplotlib.ticker import AutoMinorLocator
from scipy import integrate
from scipy.interpolate import InterpolatedUnivariateSpline

asda = {'names': ('time', 'fx-', 'fx+', 'fy-', 'fy+', 'fz-', 'fz+', 'mdot', 'counter'),
        'formats': ('f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4')}

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

r = np.loadtxt("/home/artem/Desktop/results/line2.txt", dtype=asda)

r = np.sort(r, order='time')
time = r['time']
r['fy+'] = abs(r['fy+'] + 2.85303e+10)  # + 2.665e10
r['fy-'] = abs(r['fy-'] - 3.68871e+10)  # - 2.83e10

# line1.5
# r['fy+'] = abs(r['fy+'] + 2.72945e+10)   #+ 2.665e10
# r['fy-'] = abs(r['fy-'] - 3.60181e+10)   #- 2.83e10

# line2
# r['fy+'] = abs(r['fy+'] + 1.80703e+10)   #+ 2.665e10
# r['fy-'] = abs(r['fy-'] - 3.11791e+10)   #- 2.83e10


# line5
# r['fy+'] = abs(r['fy+'] + 1.64660e+10)   #+ 2.665e10
# r['fy-'] = abs(r['fy-'] - 2.96808e+10)   #- 2.83e10

# #line4
# r['fy+'] = abs(r['fy+'] + 1.75076e+10)   #+ 2.665e10
# r['fy-'] = abs(r['fy-'] - 2.30750e+10)   #- 2.83e10

# #line3
# r['fy+'] = abs(r['fy+'] + 2.69070e+10)   #+ 2.665e10
# r['fy-'] = abs(r['fy-'] - 2.76322e+10)   #- 2.83e10

mdot = r['fx-'] + r['fx+'] + r['fy-'] + r['fy+']  # + r['fz-'] + r['fz+']
# plt.plot(time,  r['mdot'])

# figure = plt.figure(figsize=(6, 4))
# plt.subplot(2, 1, 1)
# plt.plot(time, r['fy+'])
# 
# plt.subplot(2, 1, 2)
# plt.plot(time, r['fy-'])

plt.tick_params(axis='both', which='major', labelsize=18)

plt.plot(time, r['fy-'], linewidth=2, color='black')

plt.title(r"Line2 y Flux")

plt.xlabel(r'Time', **axis_font)
plt.ylabel(u'Flux (g/s)', **axis_font)

plt.tick_params(which='minor', length=4)
plt.tick_params(which='major', length=6)

print np.mean(r['fy-'])

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
plt.show()
