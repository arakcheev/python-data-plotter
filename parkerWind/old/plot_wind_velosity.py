import numpy as np
import math
import matplotlib.pyplot as plt
import wind

Rs = 6.9598e10  # radius of Sun

radius_normalisation = Rs
# radius_normalisation = 1e11

radiuses = np.array([x for x in xrange(2, 50)])
# radiuses = np.array([x for x in xrange(5, 160)])

temperatures = np.array([0.75, 1.0, 1.5, 2.0, 3.0]) * 1.0e6

f, ax = plt.subplots()
ax.set_title('WASP-12 Wind for different temperatures')

for temp in temperatures:
    velosities = [wind.get(x * radius_normalisation, temp) for x in radiuses]
    ax.plot(radiuses, velosities, label="T = " + str(temp / 1e6) + "x$10^6$K")

# velosities = [solve(x * radius_normalisation, 0.73e6) for x in radiuses]
# ax.plot(radiuses, velosities, label="T = " + str(0.73e6 / 1e6) + "x$10^6$K")

plt.xticks(np.arange(0, 50, 2.5))
# plt.xticks(np.arange(0, 160, 20))
plt.yticks(np.arange(0, 300, 100.0))
plt.grid(b=True, which='both', color='0.65', linestyle='-')
# 
plt.axvline(x=4.9, ymin=0, ymax=500, linewidth=2, color='k', label='planet')
plt.axvline(x=2.35, ymin=0, ymax=500, linestyle='--', color='k', label='domain')
plt.axvline(x=8.3, ymin=0, ymax=500, linestyle='--', color='k')
# 
plt.xlabel('R, Rs', fontsize=20)
plt.ylabel('$u(r)$, km/s', fontsize=20)
ax.xaxis.set_label_coords(0.5, -0.05)
# 
legend = ax.legend(loc='upper left', shadow=True, bbox_to_anchor=(1, 1))
# 
plt.show()
