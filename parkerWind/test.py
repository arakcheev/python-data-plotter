import radialVelocity
import alphenRadius
import old.wind as oldWind
import old.alphen_radius as alphen_radius
import numpy as np
import matplotlib.pyplot as plt
import params
import b as B
import plotFromData

temperatures = np.array([0.75, 1.0, 1.5, 2.0, 3.0]) * 1.0e6

radiuses = [r for r in np.linspace(8, 50, 100)]

# print alphenRadius.get(7.3e5)


# plt.plot(radiuses, [alphenRadius.get(2e6) for r in radiuses] )
# plotFromData.plot(plt)
# plt.plot(radiuses, [oldWind.get(r*params.PlanetRadius, 2e6) for r in radiuses] )

# plt.plot(temperatures, [alphenRadius.get(t)/params.au for t in temperatures])
# plt.plot(temperatures, [alphen_radius.get(t)/params.au for t in temperatures])
#
# plt.show()

# plt.plot(radiuses, [B.phi(r*params.PlanetRadius, 2e6) for r in radiuses])
plt.show()
