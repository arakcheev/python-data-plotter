import math
import params
from params import *
import numpy as np
import radialVelocity
import b as B


def windDensity(r):
    return WindDensity * np.square(Separation / r)


def Lambda(r, t):
    a = np.sqrt(4 * np.pi * windDensity(r)) * radialVelocity.getsgs(r, t)
    b = B.rad(r)
    return (a / b)


# to test with nurgush code
def lambda2(r, t):
    l = np.square(Lambda(r, t))
    ra = get(t)
    return l * (1 - np.square(ra / r)) / (1 - l)


def dlp(r, t):
    return params.SolarOmega * r / radialVelocity.getsgs(r, t)


# return alphen radius in cm
def get(t):
    def eq(r):
        return Lambda(r, t) - 1

    left = StarRadius
    right = left * 500
    middle = (left + right) / 2.0
    err = eq(middle)
    index = 0
    while math.fabs(err) > params.accuracy:
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
