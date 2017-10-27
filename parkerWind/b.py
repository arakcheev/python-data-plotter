from params import *
import numpy as np
import radialVelocity
import alphenRadius


def rad(r):
    return StarInduction * np.square(StarRadius / r)


def phi(r, t):
    Ra = alphenRadius.get(t)
    return rad(r) * SolarOmega * r / radialVelocity.getsgs(r, t) * np.square(alphenRadius.Lambda(r, t)) \
           * (1 - np.square(Ra / r)) / (1 - np.square(alphenRadius.Lambda(r, t)))
