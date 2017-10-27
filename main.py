__author__ = 'artem'
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

pi = 3.14159265
mp = 1.6726231e-24

nw = 1.0e4
vw = 1.0e7

rhow = mp * nw

Separation = 7.098996e+11
primaryL1 = 0.0555591

nuj = 1.56e30

rj = 6991100000

rl1 = 4.71


def geNu(r, k):
    return math.sqrt(4.0 * pi * k * rhow) * vw * pow(r, 3.0) / nuj


r_range = xrange(2, 10, 1)

nu = [geNu(r * rj, 1) for r in r_range]
nu2 = [geNu(r * rj, 2) for r in r_range]
nu3 = [geNu(r * rj, 3) for r in r_range]
nu4 = [geNu(r * rj, 4) for r in r_range]
nu10 = [geNu(r * rj, 100) for r in r_range]

plt.plot(r_range, nu, label="Va")
plt.plot(r_range, nu2, label="2Va")
plt.plot(r_range, nu3, label="3Va")
plt.plot(r_range, nu4, label="4Va")
plt.plot(r_range, nu10, label="100Va")

plt.axvline(rl1)

plt.legend(loc=0, borderaxespad=0.)

plt.show()
