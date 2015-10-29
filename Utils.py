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
