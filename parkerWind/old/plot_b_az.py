import wind
import math
import numpy as np
import matplotlib.pyplot as plt
import params
import b_az
import b_rad

temp = 0.75e6

f, ax = plt.subplots()
ax.set_title("Azimuthal magnetic field (T=" + str(temp) + ")")

rs = np.array([x for x in xrange(2, 210)]) * params.r_sun
plt.plot(rs / params.r_sun, [b_az.bphi(r, temp) for r in rs], label=r"alfven speed for density model 1")
plt.plot(rs / params.r_sun, [b_rad.br(r) for r in rs], label=r"alfven speed for density model 1")

# plt.xlabel('R, Rs', fontsize=20)
# plt.ylabel(r"u (km/s)", fontsize=20)
# ax.xaxis.set_label_coords(0.5, -0.05)
# plt.grid(b=True, which='both', color='0.65', linestyle='-')
# legend = ax.legend(loc='upper left', shadow=True, bbox_to_anchor=(1, 1))
plt.show()
