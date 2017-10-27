import wind
import math
import numpy as np
import matplotlib.pyplot as plt
import params
import b_rad
import alphen_radius


def bphi(r, t):
    ra = alphen_radius.get(t)
    va = wind.getsgs(ra, t)
    MA = wind.getsgs(r, t) / alphen_radius.alphen_speed_sgs(r, t)
    return b_rad.br(r) * params.omega * r / va * (ra ** 2 - r ** 2) / (ra ** 2 * (1 - MA ** 2))


def v_phi(r, t):
    ra = alphen_radius.get(t)
    va = wind.getsgs(ra, t)
    MA = wind.getsgs(r, t) / alphen_radius.alphen_speed_sgs(r, t)
    return params.omega * r / va * (va - wind.getsgs(r, t)) / (1 - MA ** 2)
