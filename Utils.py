__author__ = 'artem'

import Parameters
import math

params = Parameters.Parameters

# Get roche potential value for  current position
def roche(x, y, z):
    qr10 = math.sqrt(x * x + y * y + z * z)
    qr1 = qr10
    qr20 = math.sqrt((x - params.ab) ** 2 + y ** 2 + z ** 2)
    qr2 = qr20
    return -params.prop * params.gravitationMass / qr1 - (1 - params.prop) * params.gravitationMass / qr2 - 0.5 * (
        (x - (1 - params.prop) * params.ab) ** 2 + y ** 2) * params.omega ** 2


def make_set(seq, idfun=None):
    # order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result


def get_index(array, value):
    for i in range(0, array.__len__()):
        if array[i] == value:
            return i
