import numpy as np
from numpy import log
import scipy.optimize
import matplotlib.pyplot as plt
import plotFromData

kB = 1.380622e-16
mp = 1.672623e-24
G = 6.670000e-08
KM_S_TO_SM_S = 1e5
SolarRadius = 6.959800e+10
SolarMass = 1.989000e+33
au = 1.495979e+13

# Wasp
StarRadius = 1.599 * SolarRadius
StarMass = 1.35 * SolarMass

# Solar
# StarRadius = 1.0 * SolarRadius
# StarMass   = 1.0 * SolarMass

PlanetRadius = 1.183166e+10

Separation = 3.410302e+11
# Separation = au

SolarOmega = 6.45e-6

StarInduction = 2
StarInductionRadius = StarRadius
WindDensity = 1.000000e+04 * mp

# Tw = 7.3e5
Tw = 2e6
# Tw = 2.0e6

cs = np.sqrt(2 * kB * Tw / mp)

rs = G * StarMass / (2 * np.square(cs))

print rs

CS = cs ** 2
RS = rs ** 2


def left(u):
    U = u ** 2
    return U - log(U)


def right(r):
    a = 1.0 * r
    return 4 * log(a) + 4 / a - 3


def velosityEq(c):
    assert c >= 1

    def ll(u):
        return left(u) - c

    return ll


import math


def rootsearch(f, a, b, dx):
    x1 = a;
    f1 = f(a)
    x2 = a + dx;
    f2 = f(x2)
    while f1 * f2 > 0.0:
        if x1 >= b:
            return None, None
        x1 = x2;
        f1 = f2
        x2 = x1 + dx;
        f2 = f(x2)
    return x1, x2


def bisect(f, x1, x2, switch=0, epsilon=1.0e-9):
    f1 = f(x1)
    if f1 == 0.0:
        return x1
    f2 = f(x2)
    if f2 == 0.0:
        return x2
    if f1 * f2 > 0.0:
        print('Root is not bracketed')
        return None
    n = int(math.ceil(math.log(abs(x2 - x1) / epsilon) / math.log(2.0)))
    for i in range(n):
        x3 = 0.5 * (x1 + x2);
        f3 = f(x3)
        if (switch == 1) and (abs(f3) > abs(f1)) and (abs(f3) > abs(f2)):
            return None
        if f3 == 0.0:
            return x3
        if f2 * f3 < 0.0:
            x1 = x3
            f1 = f3
        else:
            x2 = x3
            f2 = f3
    return (x1 + x2) / 2.0


def roots(f, a, b, eps=1e-6):
    root1 = 0
    root2 = 0
    while 1:
        x1, x2 = rootsearch(f, a, b, eps)
        if x1 != None:
            a = x2
            root = bisect(f, x1, x2, 1)
            if root != None:
                pass
                if (root1 == 0.0):
                    root1 = root
                    # print "root1", root1
                else:
                    root2 = root
                    # print "root2", root2, root

                if (root1 != 0.0 and root2 != 0.0):
                    break
        else:
            print ('\nDone')
            break
    return root1, root2


def getVelocity(r):
    c = right(r)
    u1, u2 = roots(velosityEq(c), 1e-5, 5)  # bound in CS
    maxU = max(u1, u2)
    minU = min(u1, u2)
    if (r > 1.0):
        return maxU
    else:
        return minU


def getVelocity1(r):
    return RS / (r ** 2) * np.exp(3.0 / 2 - 2 * rs / r) * cs
    # return np.sqrt(4* np.log(r/ rs) - 0)* cs


def getWindDensity(r):
    return WindDensity * np.square(Separation / r)


def windBr(r):
    return StarInduction * np.square(StarRadius / r)


def lambda_(r):
    rr = r[0]
    a = np.sqrt(4 * np.pi * getWindDensity(rr)) * getVelocity1(rr)
    b = windBr(rr)
    return (a / b)


# sol = scipy.optimize.root(lambda_, [100 * PlanetRadius])

Ra = 5.17859167e+12


# print Ra

def vphi(r):
    return SolarOmega * r * (1 - np.square(lambda_([r]) * Ra / r)) / (1 - lambda_([r]) ** 2)


def bphi(r):
    return windBr(r) * SolarOmega * r / getVelocity1(r) * np.square(lambda_([r])) \
           * (1 - np.square(Ra / r)) / (1 - lambda_([r]) ** 2)


linspace = [r for r in np.linspace(7, 50, 100)]

# a = [ lambda_(r*PrimaryRadius)   for r in linspace]

# print roots(lambda_, 50*PrimaryRadius, 500*PrimaryRadius)


# plt.plot(linspace, [bphi(r * PlanetRadius) for r in linspace])
# plt.plot(linspace, [windBr(r * PlanetRadius) for r in linspace])
# plt.plot(linspace, b)
# plotFromData.plot(plt)
# plt.plot(linspace, velicities)
# plt.show()
