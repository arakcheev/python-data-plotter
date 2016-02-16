__author__ = 'artem'

import sys
from FileData import FileData
from TecData import TecData
from Parameters import Parameters
import glob
import matplotlib.pyplot as plt
import os
import re

# folder = "/Users/artem/workspace/inasan/nurgushmpi/bin/data/"
folder = "/Volumes/Storage/workspace/inasan/nurgush/exp_grid/"
# folder = ""
pattern = "a5000.dat"
target = folder + "contour/"

try:
    arg_name = sys.argv[1]
    folder = ""
    pattern = arg_name
except Exception:
    ""  # nothing

if not os.path.exists(target):
    os.makedirs(target)

files = glob.glob(folder + pattern)

# initial_data = FileData(folder + "a0.dat")

n = 0
totalFiles = float(files.__len__())


def calc_staff(i):
    file_name = files[i]
    print "Plot file  (" + "{0:.2f}".format(i / totalFiles * 100) + "%) " + str(file_name)

    groups = re.search('(.*)a(.*).dat', file_name)

    file_data = TecData(file_name)

    figure, ax = plt.subplots()

    file_data.plot_contour(ax)
    file_data.plot_roche_lobe(ax)
    file_data.plot_velocity_filed(ax)

    figure.suptitle('T=7500, time = ' + "{:.2}".format(file_data['time']))

    # plt.savefig(target + "contour_" + groups.group(2) + '.png')
    plt.show()
    plt.close(figure)


calc_staff(0)
# import multiprocessing; pool = multiprocessing.Pool(4); pool.map(calc_staff, range(0, files.__len__()))
