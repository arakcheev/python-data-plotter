# coding=utf-8
import math
import numpy as np
import matplotlib.pyplot as plt
import params
import wind


def rho1(r):
    return params.rho0 * (params.r0 / r) ** 2


def rho2(r):
    return params.normalize_m_dot / (4 * math.pi * wind.get(r, 0.75e6) * 1e5 * r ** 2)


rs = np.array([x for x in xrange(2, 15)]) * params.r_sun

f, ax = plt.subplots()
ax.set_title("Solar wind density")

## See 1.2 factor from http://articles.adsabs.harvard.edu/cgi-bin/nph-iarticle_query?1988ApJ...325..442W&amp;data_type=PDF_HIGH&amp;whole_paper=YES&amp;type=PRINTER&amp;filetype=.pdf article 
plt.plot(rs / params.r_sun, [math.log10(1.2 * rho1(r) / 1.66e-24) for r in rs], label=r"~$r^{-2}$")
plt.plot(rs / params.r_sun, [math.log10(1.2 * rho2(r) / 1.66e-24) for r in rs], label=r"~$v^{-1}r^{-2}$")

plt.xlabel('R, Rs', fontsize=20)
plt.ylabel(r"$log(N)$", fontsize=20)
ax.xaxis.set_label_coords(0.5, -0.05)
plt.grid(b=True, which='both', color='0.65', linestyle='-')
legend = ax.legend(loc='upper left', shadow=True, bbox_to_anchor=(1, 1))
plt.show()
