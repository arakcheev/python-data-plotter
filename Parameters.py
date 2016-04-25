__author__ = 'artem'

import math

import ConfigParser

Config = ConfigParser.ConfigParser()
Config.read("parameters.cfg")


class Parameters:
    def __init__(self):
        pass

    sunRadius = Config.getfloat("sun", "radius")
    earthRadius = Config.getfloat("earth", "radius")
    earthMass = Config.getfloat("earth", "mass")
    sunMass = Config.getfloat("sun", "mass")

    planet_radius = Config.getfloat("planet", "radius") * earthRadius

    dmass_1 = Config.getfloat("common", "dmass_1") * sunMass
    dmass_2 = Config.getfloat("common", "dmass_2") * earthMass
    
    q_prop = dmass_1 / dmass_2
    prop = q_prop / (q_prop + 1.0)

    gravitationMass = Config.getfloat("common", "gravity") * (dmass_1 + dmass_2)
    ab = Config.getfloat("planet", "separation") * 1.49597892e13
    
    omega = math.sqrt(gravitationMass / ab ** 3)
    period = 2. * math.pi / omega
