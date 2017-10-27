import math
import params
from params import *
import numpy as np


# Must return speed in km/s
def sound_speed(t):
    return np.sqrt(2 * kB * t / mp) / 1e5


# Must return radius in cm
def sonic_radius(t):
    return G * StarMass / (2 * np.square(sound_speed(t) * 1e5))


def right_part(r, t):
    rs = sonic_radius(t)
    return 4.0 * math.log(1.0 * r / rs) + 4.0 * rs / r - 3


def left_part(u, t):
    cs = sound_speed(t)
    uu = 1.0 * np.square(u / cs)
    return uu - math.log(uu)


# Return speed in km/s
def get(r, t):
    rp = right_part(r, t)
    rs = sonic_radius(t)

    cs = sound_speed(t)

    if r < rs:
        left = 0.1
        right = cs
    else:
        left = cs
        right = 1000

    def eq(u):
        return left_part(u, t) - rp

    middle = (left + right) / 2
    err = eq(middle)
    index = 0
    while math.fabs(err) > accuracy:
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


def getsgs(r, t):
    return get(r, t) * 1e5
