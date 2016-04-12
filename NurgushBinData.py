__author__ = 'artem'

import numpy as np
from spacepy import dmarray
from Model import Model
import Parameters
import struct

params = Parameters.Parameters


class NurgushBinData(Model):
    def sub_title(self):
        return ' time = ' + "{:.2}".format(self['time']) + " "

    def get_name(self):
        return str(self['iter'])

    def __init__(self, file_name, *args, **kwargs):
        super(NurgushBinData, self).__init__(*args, **kwargs)  # Init as PbData
        self.attrs['file'] = file_name
        self.read()
        self['log_rho'] = np.log(self['rho'])

    def read(self):
        _file = open(self.attrs['file'], 'rb')
        endian = '<'

        reclen_raw = _file.read(4)

        rec_len = struct.unpack(endian + 'i', reclen_raw)[0]
        if rec_len > 10000 or rec_len < 0:
            endian = '>'
            rec_len = struct.unpack(endian + 'i', reclen_raw)[0]

        variables = _file.read(rec_len)
        names = [var.strip().lower() for var in variables.split(",") if var.__len__() > 0]
        names[-1] = 'hz'

        self['time'] = struct.unpack(endian + 'd', _file.read(8))[0]
        self['iter'] = struct.unpack(endian + '2i', _file.read(8))[0]

        (I, J, K) = struct.unpack('3l', _file.read(24))
        self["ndim"] = 3
        self['grid'] = dmarray(np.array([I, J, K]))
        self['grid'].attrs['gtype'] = 'Exponential'
        self['grid'].attrs['nx'] = I
        self['grid'].attrs['ny'] = J
        self['grid'].attrs['nz'] = K

        temp_data = dict()

        for i in range(0, names.__len__()):
            name = names[i].lower()
            temp_data[name] = np.zeros(self['grid'])

        for k in xrange(0, self['grid'][2]):
            for j in xrange(0, self['grid'][1]):
                for i in xrange(0, self['grid'][0]):
                    # TODO: Magic number 15
                    data = struct.unpack(endian + '15d', _file.read(names.__len__() * 8))
                    for ii in range(0, names.__len__()):
                        temp_data[names[ii]][i, j, k] = data[ii]

        _file.close()
        print "file closed"

        __dim = 2

        normalization = params.ab / params.planet_radius

        k_middle = 0

        if __dim == 2:
            k_middle = self['grid'][2] / 2
            self['x'] = temp_data['x'][:, 0, k_middle] * normalization
            tmp = np.zeros(self['grid'][1])
            for j in range(0, self['grid'][1]):
                tmp[j] = temp_data['y'][0, j, k_middle]
                self['y'] = tmp * normalization

        if __dim == 3:
            self['x'] = temp_data['x'] * normalization
            self['y'] = temp_data['y'] * normalization
            self['z'] = temp_data['z'] * normalization

        for i in range(3, names.__len__()):
            name = names[i].lower()
            if __dim == 2:
                self[name] = np.zeros((self['grid'][1], self['grid'][0]))
            if __dim == 3:
                self[name] = np.zeros((self['grid'][0], self['grid'][1], self['grid'][2]))

        gen = (name for name in names if name not in ['x', 'y', 'z'])

        print "start fill"

        for k in range(0, self['grid'][2]):
            for j in range(0, self['grid'][1]):
                for i in range(0, self['grid'][0]):
                    for name in gen:
                        if __dim == 2:
                            self[name][i, j] = temp_data[name][i, j, k_middle]
                        if __dim == 3:
                            self[name][i, j, k] = temp_data[name][i, j, k]

        del temp_data
