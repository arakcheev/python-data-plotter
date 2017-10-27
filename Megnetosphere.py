# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
from math import sin
from math import pi
from matplotlib.ticker import AutoMinorLocator
from scipy import integrate
from scipy.interpolate import InterpolatedUnivariateSpline

G = 6.670000e-08
# Moment
MomentJ = 1.56e30  # / (Induction * Length**3)
Moment = 0.1 * MomentJ

Density = 1.672623e-20 * 1.1417
# Velocity=10101106.9815
Velocity = 2.45 * 1e7
# Velocity=23490946.4685

AtmDensity = 2.676197e-14

Rg = 8.314e7
gamma = 5.0 / 3.0
Tw = 7.3e5
epsw = Rg * Tw / (gamma - 1)

Pw = (gamma - 1) * Density * epsw
Pd = Density * Velocity ** 2 / 2

P = Pd + Pw

PrimaryMass = 2.585700e+30
PrimaryRadius = 1.183166e+10


def m_pres(theta, r):
    return (Moment ** 2) / (r ** 6) * (3 * sin(theta) ** 2 + 1) / (8 * pi)


def Rm(theta):
    r = (Moment ** 2) / (8 * pi * P) * (3 * sin(theta) ** 2 + 1)
    return (r ** (1.0 / 6)) / PrimaryRadius


def atmPressure(R, T):
    k = - G * PrimaryMass / (Rg * T)
    atm = k * (1.0 / PrimaryRadius - 1.0 / R)
    return AtmDensity * np.exp(atm) * Rg * T


def findInsidePressureBoundary(t, theta):
    def eq(r):
        return atmPressure(r, t) - m_pres(theta, r)

    left = 0.75 * PrimaryRadius
    right = 1.5 * PrimaryRadius
    middle = (left + right) / 2.0
    err = eq(middle)
    index = 0
    while np.fabs(err) > 1e-6:
        if eq(left) * eq(middle) < 0:
            right = middle
        else:
            left = middle
        middle = 1.0 * (left + right) / 2.0
        err = eq(middle)
        index += 1
        if index == 1000:
            break

    return middle


angles = np.arange(0, 90, 1)
rms = [Rm(a * pi / 180) for a in angles]

# print "Radius =", findInsidePressureBoundary(8200, 0)/PrimaryRadius
# print "Radius =", findInsidePressureBoundary(8200, 15*pi/180)/PrimaryRadius
# print "Radius =", findInsidePressureBoundary(8200, 30*pi/180)/PrimaryRadius

print np.cos(90 * pi / 180)

# print np.log(m_pres(30*pi/180, 1.46*PrimaryRadius)*8*pi/(1.051148e-02*1.051148e-02))

# radiuses = [r * PrimaryRadius for r in np.arange(0.75, 1.5, 0.01)]
# plt.plot([r/PrimaryRadius for r in radiuses], [np.log10(atmPressure(r, 8200)) for r in radiuses])
# plt.plot([r/PrimaryRadius for r in radiuses], [np.log10(m_pres(0, r)) for r in radiuses])

# plt.plot(angles, [findInsidePressureBoundary(8200, t*pi/180)/PrimaryRadius for t in angles])
# plt.plot(angles, rms)
# plt.plot((0, 90), (1.92, 1.92))
# # plt.plot(angles, [m_pres(t*pi/180, PrimaryRadius) for t in angles])
# plt.show()

# for t in angles:
# print "Pressure %e and %e" % (m_pres(30, 1.9273*PrimaryRadius), P)
# print "Pressure %e and %e" % (m_pres(10, 2*PrimaryRadius), P)

#
# f = open('./data/magnetosphere_1.txt', 'w')
# f.write('TITLE = "Magnetosphere radius"\n')
# f.write('Variables="Theta","Rm"\n')
# f.write('Zone I={:d}, F=POINT\n'.format(angles.__len__()))
# for i in angles:
#     rm = Rm(i*pi/180)
#     f.write("{:4d} {:4f}\n".format(i, rm))
# f.close()
#
# plt.plot(angles, rms)
# plt.show()
