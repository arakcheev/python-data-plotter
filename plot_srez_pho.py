__author__ = 'artem'

import os
from FileData import FileData
from Parameters import Parameters
import glob
import matplotlib.pyplot as plt

folder = "test_data/"
pattern = "*.out"
target = folder + "srez_rho/"

if not os.path.exists(target):
    os.makedirs(target)

files = glob.glob(folder + pattern)

initial_data = FileData(files.pop(0))

n = 0
totalFiles = float(files.__len__())


def calc_staff(i):
    file_name = files[i]
    print "Plot file  (" + "{0:.2f}".format(i / totalFiles * 100) + "%) " + str(file_name)
    file_data = FileData(file_name)
    figure, ax = plt.subplots()

    file_data.srez_y('rho', -0.8, ax, initial_data, [-100, 30])
    ax.set_xticks(file_data['x'], minor=True)
    ax.set_yticks(file_data['y'], minor=True)
    ax.set_ylabel("y=-0.4")

    figure.suptitle('T=7500, time = ' + str(file_data.attrs['time'] / Parameters.period))

    plt.savefig(target + "srez_" + str(file_data.attrs['iter']) + '.png')
    plt.close(figure)


import multiprocessing

pool = multiprocessing.Pool(4)

pool.map(calc_staff, range(0, files.__len__()))
