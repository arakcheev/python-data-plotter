import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.optimize import minimize

import wind

vels = np.array([x for x in xrange(1, 200)])
v = [wind.left_part(u, 0.73e6) for u in vels]

plt.plot(vels, v)
plt.show()
