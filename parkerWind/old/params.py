r_sun = 6.9598e10
m_sun = 2e33  # gram
au = 1.49597892e13
year = 31556952  # seconds
accuracy = 1e-6

# wind
rho0 = 1.0e4 * 1.66e-24
r0 = 10.1 * r_sun
# rho0 = 10*1.66e-24
# r0 = au

# star
# STAR_MASS = 1.0  # sun mass
STAR_MASS = 1.35  # sun mass
m_dot = 2e-14  # sun mass per year
field = 1  # gauss
radius = 1.2 * r_sun
# radius = r_sun
omega = 6e-6  # 1/sec

normalize_m_dot = m_dot * m_sun / year
