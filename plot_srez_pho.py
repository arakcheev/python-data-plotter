__author__ = 'artem'

import sys
import os
from TecData import TecData
from Parameters import Parameters
import glob
import matplotlib.pyplot as plt

folder = "/Volumes/Storage/workspace/inasan/nurgush/exp_grid/"
pattern = "*.dat"
target = folder + "slices/"

if not os.path.exists(target):
    os.makedirs(target)


files = glob.glob(folder + pattern)

# initial_data = FileData(files.pop(0))

n = 0
totalFiles = float(files.__len__())


def calc_staff(i):
    file_name = files[i]
    print "Plot file  (" + "{0:.2f}".format(i / totalFiles * 100) + "%) " + str(file_name)
    file_data = TecData(file_name)

    figure, (ax1, ax2) = plt.subplots(2)

    (_, y) = file_data.srez_y('log_rho', 3.0, ax1)
    ax1.set_ylabel(r"rho")
    ax1.grid(which='both')
    # ax1.set_xlim([-15, 15])

    # file_data.srez_y('T', 3.0, ax2)
    # ax2.set_ylabel("p/rho")
    # ax2.grid(which='both')
    # ax2.set_xlim([-15, 15])

    figure.suptitle('T=7500, time = ' + "{:.2}".format(file_data['time']))

    # figure.set_size_inches(10.5, 18.5, forward=True)

    # plt.savefig(target + "slice_" + str(file_data.attrs['iter']) + '.png')
    plt.show()
    plt.close(figure)


calc_staff(0)
# import multiprocessing; pool = multiprocessing.Pool(4); pool.map(calc_staff, range(0, files.__len__()))

# target = "/Volumes/Storage/workspace/inasan/SWMF/results13.01.16/sliceComparison/logT/"
# 
# folder_075 = "/Volumes/Storage/workspace/inasan/SWMF/results13.01.16/075R/data/*.out"
# folder_1 = "/Volumes/Storage/workspace/inasan/SWMF/results13.01.16/1.0R/data/*.out"
# folder_original = "/Volumes/Storage/workspace/inasan/SWMF/results13.01.16/original/data/*.out"
# 
# files_075 = glob.glob(folder_075)
# files_1 = glob.glob(folder_1)
# files_original = glob.glob(folder_original)
# 
# 
# def sliceComparison(i):
#     file_name_075 = files_075[i]
#     file_name_1 = files_1[i]
#     file_name_original = files_original[i]
# 
#     file_data_075 = FileData(file_name_075)
#     file_data_1 = FileData(file_name_1)
#     file_data_original = FileData(file_name_original)
# 
#     figure, ax1 = plt.subplots()
# 
#     file_data_075.srez_y('T', 0.2, ax1, y_limit=[2, 7], label='0.75R')
#     # ax1.set_title('O.75 Rpl, time = ' + "{:.5}".format(file_data_075.attrs['time'] / Parameters.period))
#     
#     # file_data_1.srez_y('T', 0.2, ax2, y_limit=[-14.5, -3])
#     # ax2.set_title('1.0 Rpl, time = ' + "{:.5}".format(file_data_1.attrs['time'] / Parameters.period))
#     
#     file_data_original.srez_y('T', 0.2, ax1, y_limit=[2, 7],  label='Original')
#     
#     ax1.grid(which='both')
#     
#     legend = ax1.legend(loc='upper right', shadow=True)
# 
#     # ax2.set_title('Original, time = ' + "{:.5}".format(file_data_original.attrs['time'] / Parameters.period))
#     
#     
#     # ax2.grid(which='both')
#     # ax3.grid(which='both')
# 
#     # file_data.srez_y('T', 0.2, ax3, y_limit=[-14.5, -3])
#     # ax3.set_ylabel("p/rho")
#     # ax3.grid(which='both')
# 
#     figure.suptitle('Slices T=7500, time = ' + "{:.2}".format(file_data_075.attrs['time'] / Parameters.period))
# 
#     # figure.set_size_inches(10.5, 18.5, forward=True)
# 
#     plt.savefig(target + "slice_" + str(file_data_075.attrs['iter']) + '.png')
#     # plt.show()
#     plt.close(figure)
# 
# 
# import multiprocessing; pool = multiprocessing.Pool(4);pool.map(sliceComparison, range(0, files_original.__len__())) 
# # sliceComparison(10)
