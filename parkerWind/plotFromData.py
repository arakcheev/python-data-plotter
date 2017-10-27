import numpy as np
from matplotlib.ticker import AutoMinorLocator
import params

asda = {'names': ('r', 'u'),
        'formats': ('f4', 'f4')}


def plot(plt):
    from matplotlib import rc
    rc('font', **{'family': 'serif', 'serif': ['Roboto']})
    rc('text', usetex=True)
    rc('text.latex', unicode=True)
    data = np.sort(np.loadtxt("./wasp.data", dtype=asda))

    r = data['r'] / params.PlanetRadius

    plt.plot(r, data['u'] / 1e5)
    # plt.show()
