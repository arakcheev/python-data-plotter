__author__ = 'artem'

import math

import ConfigParser

Config = ConfigParser.ConfigParser()
Config.read("parameters.cfg")


class Parameters:
    def __init__(self):
        pass

    sunRadius = Config.getfloat("sun", "radius")
    planet_radius = Config.getfloat("planet", "radius") * sunRadius
    sunMass = Config.getfloat("sun", "mass")
    dmass_1 = Config.getfloat("common", "dmass_1") * sunMass
    dmass_2 = Config.getfloat("common", "dmass_2")  # 0.0006*dmsun
    q_prop = dmass_1 / dmass_2
    prop = q_prop / (q_prop + 1.0)
    gravitationMass = Config.getfloat("common", "gravity") * (dmass_1 + dmass_2)
    ab = Config.getfloat("planet", "separation")  # /rpl!10.1*rsun
    omega = math.sqrt(gravitationMass / ab ** 3)
    period = 2. * math.pi / omega
