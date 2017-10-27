import wind
import math
import numpy as np
import matplotlib.pyplot as plt
import params


def br(r):
    return params.field * params.radius ** 2 / r ** 2
