__author__ = 'artem'

import numpy as np
import re
from spacepy import dmarray
from Model import Model
import Parameters

params = Parameters.Parameters


class TecData(Model):
    def __init__(self, file_name, *args, **kwargs):
        super(TecData, self).__init__(*args, **kwargs)  # Init as PbData
        self.attrs['file'] = file_name
        self.read()
        self['log_rho'] = np.log(self['rho'])

    def __extract_variables(self, str):
        return re.search('VARIABLES = (.*)', str).group(1).replace('"', '').split(", ")

    def __extract_zone(self, str):
        groups = re.search('ZONE T="(.*)", I=(.*), J=(.*), K=(.*), F=(.*)', str)

        I = int(groups.group(2))
        J = int(groups.group(3))
        K = int(groups.group(4))

        self["ndim"] = 3
        self['grid'] = dmarray([I, J, K])
        self['grid'].attrs['gtype'] = 'Exponential'
        self['grid'].attrs['nx'] = I
        self['grid'].attrs['ny'] = J
        self['grid'].attrs['nz'] = K

    def __extract_aux_data(self, file):
        for i in range(0, 1):
            line = file.readline()
            groups = re.search('AUXDATA (.*) = "(.*)"', line)

            if groups.group(1).lower() == "time":
                self['time'] = float(groups.group(2))

    def read(self):
        f = open(self.attrs['file'])
        # self.attrs['title'] = self.__extract_from_string(f.readline())
        names = map(str.lower, self.__extract_variables(f.readline()))
        self.__extract_zone(f.readline())
        self.__extract_aux_data(f)

        temp_data = dict()

        for i in range(0, names.__len__()):
            name = names[i].lower()
            temp_data[name] = dmarray(np.zeros(self['grid']))

        # Read 3d data
        for k in range(0, self['grid'][2]):
            for j in range(0, self['grid'][1]):
                for i in range(0, self['grid'][0]):
                    data = f.readline().split()
                    for ii in range(0, names.__len__()):
                        temp_data[names[ii]][i, j, k] = data[ii]

        f.close()

        # Fill 2d data to plotting                
        k_middle = self['grid'][2] / 2

        # Units in planet radii
        self['x'] = temp_data['x'][:, 0, k_middle] * params.ab / params.planet_radius

        tmp = dmarray(np.zeros(self['grid'][1]))
        for j in range(0, self['grid'][1]):
            tmp[j] = temp_data['y'][0, j, k_middle]
        self['y'] = tmp * params.ab / params.planet_radius

        for i in range(3, names.__len__()):
            name = names[i].lower()
            self[name] = dmarray(np.zeros((self['grid'][1], self['grid'][0])))

        gen = (name for name in names if name not in ['x', 'y', 'z'])
        for name in gen:
            for j in range(0, self['grid'][1]):
                for i in range(0, self['grid'][0]):
                    self[name][j, i] = temp_data[name][i, j, k_middle]
