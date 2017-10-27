import wind
import math
import numpy as np
import matplotlib.pyplot as plt
import params
import b_rad


def rho1(r):
    return params.rho0 * (params.r0 / r) ** 2


def alphen_speed1(r, t):
    return b_rad.br(r) / math.sqrt(4 * math.pi * rho1(r))


def alphen_speed_sgs(r, t):
    return math.sqrt(
        params.field ** 2 * params.radius ** 4 * wind.getsgs(r, t) / (r ** 2 * params.normalize_m_dot))


def alphen_speed(r, t):
    return alphen_speed_sgs(r, t) / 1e5


def get(t):
    # return 22 * params.r_sun
    def eq(r):
        return alphen_speed1(r, t) - wind.getsgs(r, t)

    left = params.r_sun
    right = 100 * params.r_sun
    middle = (left + right) / 2
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
