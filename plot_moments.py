__author__ = 'artem'

import os
from FileData import FileData
from Parameters import Parameters
import glob
import matplotlib.pyplot as plt

folder = "/Volumes/Storage/workspace/inasan/SWMF/test/"
pattern = "*.out"
target = folder + "moments/"

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

    moments = file_data.moment_contour(ax, initial_data)

    figure.colorbar(moments)

    figure.suptitle('T=7500, time = ' + str(file_data.attrs['time'] / Parameters.period))

    plt.savefig(target + "moment_" + str(file_data.attrs['iter']) + '.png')
    # plt.show()
    plt.close(figure)


# calc_staff(0)

import multiprocessing

pool = multiprocessing.Pool(4)

pool.map(calc_staff, range(40, 100))
