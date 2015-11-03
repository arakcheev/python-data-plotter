__author__ = 'artem'

import numpy as np
from Utils import (get_index, make_set)
from spacepy.pybats import PbData


class TecData(PbData):
    def __init__(self, file_name, *args, **kwargs):
        super(TecData, self).__init__(*args, **kwargs)  # Init as PbData
        self.attrs['file'] = file_name
        self.read()

    def __extract_from_string(self, str):
        splited = str.strip().split("=")

        if splited.__len__() > 1:
            return splited[1].replace('"', '')
        else:
            return splited[0]

    def __extract_zone(self, str):
        import re

        data = str.strip().split("ZONE ")[1].split(",")

        for line in data:
            trimed = re.sub('[\s+]', '', line).split("=")
            name = trimed[0]
            value = trimed[1]

            if name == "N" or name == "E":
                self.attrs[name] = int(value)

    def __extract_aux_data(self, file):
        for i in range(0, 20):
            file.readline()

    def read(self):

        from spacepy.datamodel import dmarray

        f = open(self.attrs['file'])
        self.attrs['title'] = self.__extract_from_string(f.readline())
        self.__extract_from_string(f.readline())
        self.__extract_zone(f.readline())
        self.__extract_aux_data(f)

        # First read all data from file
        data = ['']
        for j in range(0, self.attrs['N']):
            data.append(f.readline())

        # Next read all data from file and fill grid
        indices = []
        x = []
        y = []
        for j in range(0, self.attrs['E']):
            line = f.readline()
            indices.append(line)
            line = line.strip().split()
            p1 = int(line[0])
            p3 = int(line[1])
            p2 = int(line[2])
            p4 = int(line[3])
            str1 = data[p1].strip().split()
            str2 = data[p2].strip().split()
            str3 = data[p3].strip().split()
            str4 = data[p4].strip().split()
            x1 = float(str1[0])
            y1 = float(str1[1])
            z1 = float(str1[2])
            x2 = float(str2[0])
            y2 = float(str2[1])
            z2 = float(str2[2])
            x3 = float(str3[0])
            y3 = float(str3[1])
            z3 = float(str3[2])
            x4 = float(str4[0])
            y4 = float(str4[1])
            z4 = float(str4[2])
            x.append(x1)
            y.append(y1)
            x.append(x2)
            y.append(y2)
            x.append(x3)
            y.append(y3)
            x.append(x4)
            y.append(y4)

        self['x'] = dmarray(np.sort(np.array(make_set(x))), attrs={'units': 'R'})
        self['y'] = dmarray(np.sort(np.array(make_set(y))), attrs={'units': 'R'})

        self['grid'] = dmarray([self['x'].__len__(), self['y'].__len__()])

        rho = np.zeros((self['grid'][1], self['grid'][0]))
        # ux = np.zeros(self['grid'])
        # uy = np.zeros(self['grid'])

        # Fill other data
        for j in range(0, self.attrs['E']):
            line = indices[j].strip().split()
            p1 = int(line[0])
            p3 = int(line[1])
            p2 = int(line[2])
            p4 = int(line[3])
            str1 = data[p1].strip().split()
            str2 = data[p2].strip().split()
            str3 = data[p3].strip().split()
            str4 = data[p4].strip().split()
            x1 = float(str1[0])
            y1 = float(str1[1])
            z1 = float(str1[2])
            x2 = float(str2[0])
            y2 = float(str2[1])
            z2 = float(str2[2])
            x3 = float(str3[0])
            y3 = float(str3[1])
            z3 = float(str3[2])
            x4 = float(str4[0])
            y4 = float(str4[1])
            z4 = float(str4[2])

            x1_index = get_index(self['x'], x1)
            x2_index = get_index(self['x'], x2)
            x3_index = get_index(self['x'], x3)
            x4_index = get_index(self['x'], x4)

            y1_index = get_index(self['y'], y1)
            y2_index = get_index(self['y'], y2)
            y3_index = get_index(self['y'], y3)
            y4_index = get_index(self['y'], y4)

            rho[y1_index, x1_index] = str1[3]
            rho[y2_index, x2_index] = str2[3]
            rho[y3_index, x3_index] = str3[3]
            rho[y4_index, x4_index] = str4[3]

            # ux[x1_index, y1_index] = str1[4]
            # ux[x2_index, y2_index] = str2[4]
            # ux[x3_index, y3_index] = str3[4]
            # ux[x4_index, y4_index] = str4[4]
            #
            # uy[x1_index, y1_index] = str1[5]
            # uy[x2_index, y2_index] = str2[5]
            # uy[x3_index, y3_index] = str3[5]
            # uy[x4_index, y4_index] = str4[5]

        self['rho'] = dmarray(rho)

        print self['grid']

        for j in range(0, self['grid'][1]):
            for i in range(0, self['grid'][0]):
                if self['rho'][j, i] == 0:

                    if j == 0 and i == 0:
                        self['rho'][j, i] = (self['rho'][j + 1, i]
                                             + self['rho'][j, i + 1] + self['rho'][j + 1, i + 1]) / 3
                    elif j == 0:
                        self['rho'][j, i] = (self['rho'][j + 1, i]
                                             + self['rho'][j, i - 1] + self['rho'][j, i + 1]) / 3
                    elif i == 0:
                        self['rho'][j, i] = (self['rho'][j + 1, i]
                                             + self['rho'][j - 1, i] + self['rho'][j, i + 1]) / 3
                    elif i == self['grid'][0] - 1:
                        self['rho'][j, i] = (self['rho'][j - 1, i] + self['rho'][j + 1, i]
                                             + self['rho'][j, i - 1]) / 3
                    elif j == self['grid'][1] - 1:
                        self['rho'][j, i] = (self['rho'][j - 1, i] + self['rho'][j, i + 1]
                                             + self['rho'][j, i - 1]) / 3
                    elif j == self['grid'][1] - 1 and i == self['grid'][0] - 1:
                        self['rho'][j, i] = (self['rho'][j - 1, i] + self['rho'][j, i - 1]
                                             + self['rho'][j - 1, i - 1]) / 3
                    else:
                        self['rho'][j, i] = (self['rho'][j - 1, i] + self['rho'][j + 1, i]
                                             + self['rho'][j, i - 1] + self['rho'][j, i + 1]) / 4

                        # self['ux'] = dmarray(ux)
                        # self['uy'] = dmarray(uy)
