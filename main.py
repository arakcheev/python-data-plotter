__author__ = 'artem'

import glob
import FileData
import Parameters
import matplotlib.pyplot as plt

import numpy
import Utils

import Parameters

import math

params = Parameters.Parameters

# files = glob.glob("test_data/*.out")

# outFiles = glob.glob("srez/*.png")
# n = 0
# totalFiles = float(files.__len__())
#
# initial_file = files.pop(0)
#
# initial_data = FileData.FileData(initial_file)

data = FileData.FileData("z=0_ful_1_t00001709_n00000032.out")
initial = FileData.FileData("z=0_ful_1_t00000000_n00000000.out")
# initial_data = FileData.FileData("z=0_ful_1_t00000000_n00000000.out")

# print data['grid'].attrs
figure, ax = plt.subplots()

# data.plotContour(ax)
data.moment_contour(ax, initial)

#
plt.show()

# figure, (ax1, ax2) = plt.subplots(2)
# data.srez_y('log_rho', -0.8, ax2, initial_data, [-10, 10])
# ax2.set_xticks(data['x'], minor=True)
# ax2.set_yticks(data['y'], minor=True)
# ax2.set_ylabel("y=-0.4")
# data.srez_y('log_rho', 0.4, ax1, initial_data, [-10, 10])
# ax1.set_ylabel("y=0.4")

# plt.savefig('bigResolution.png')
# plt.close(figure)

# print initial_data['rho'].attrs

# plt.rc('text', usetex=True)
# plt.rc('font', family='serif')

def calc_staff(i):
    file_name = files[i]
    print "Plot file  (" + "{0:.2f}".format(i / totalFiles * 100) + "%) " + str(file_name)
    file_data = FileData.FileData(file_name)
    figure, ax = plt.subplots()
    file_data.plotContour(ax)
    file_data.plotRocheLobe(ax)
    file_data.plotVelocityFiled(ax)
    # figure, (ax1,ax2) = plt.subplots(2)
    # file_data.srez_y('ux', -0.8, ax2, initial_data, [-100, 30])
    # ax2.set_xticks(file_data['x'])
    # ax2.set_yticks(file_data['y'])
    # ax2.set_ylabel("y=-0.4")
    # file_data.srez_y('ux', 0.4, ax1, initial_data, [-100, 30])
    # ax1.set_ylabel("y=0.4")
    # initial_data.srez_y('rho', -0.2, ax, None, [0, 1e6], 'y')

    # moments = file_data.moment_contour(ax, initial_data)
    #
    # figure.colorbar(moments)

    # file_data.plotContour(ax)
    # ax.set_xticks(file_data['x'])
    # ax.set_yticks(file_data['y'])
    # plt.grid()
    # file_data.plotRocheLobe(ax)
    # file_data.plotVelocityFiled(ax)
    # figure = file_data.srezContourVx(-0.2)
    # figure = file_data.srezRhoMinusInitial(initial_data.rho, initial_data.U, -0.2)
    figure.suptitle('T=7500, time = ' + str(file_data.attrs['time'] / Parameters.Parameters.period))

    plt.savefig('test_target/contour' + str(file_data.attrs['iter']) + '.png')
    # plt.show()
    plt.close(figure)

# import multiprocessing
#
# pool = multiprocessing.Pool(4)
#
# pool.map(calc_staff, range(0, files.__len__()))

# for i in range(0, files.__len__()):
#     calc_staff(i)

# import TecData
#
# data = TecData.TecData("z=0_ful_1_t01830640_n00171713.dat")
#
# # print data['rho'].max()
# #
# log_rho = numpy.zeros((data['grid'][1], data['grid'][0]))
#
# for j in range(0, data['grid'][1]):
#     for i in range(0, data['grid'][0]):
#         log_rho[j, i] = math.log(data['rho'][j, i])
# #
# plt.figure()
#
# rho_min = math.log(data['rho'].min())
# rho_max = math.log(data['rho'].max())
#
# levels = numpy.arange(rho_min, rho_max, 0.1)
#
# plt.contour(data['x'], data['y'], log_rho, levels)  # _levels = 30
#
# _roche = numpy.zeros((data['grid'][1], data['grid'][0]))
#
# for j in range(0, data['grid'][1]):
#     for i in range(0, data['grid'][0]):
#         _roche[j, i] = Utils.roche(data['x'][i] * params.planet_radius,
#                                    data['y'][j] * params.planet_radius, 0)
#
# # One equipotential level for piloting lobe where platen in
# roc0 = Utils.roche(params.ab - 0.547 * params.sunRadius, 0.0, 0.0)
#
# roche_levels = [roc0]
#
# plt.contour(data['x'], data['y'], _roche, roche_levels, colors="r",
#              linewidths=[2])  # plt.plot(data['x'], log_rho[:, 150])
# #
# plt.show()
#
# # Build new linspace
# x = numpy.linspace(data['x'].min(), data['x'].max(), _levels)
# y = numpy.linspace(data['y'].min(), data['y'].max(), _levels)
#
# v_x = numpy.zeros((_levels, _levels))
# v_y = numpy.zeros((_levels, _levels))
#
# for i in range(0, data['grid'][0], 10):
#     for j in range(0, data['grid'][1], 10):
#         _v = data['ux'][i, j]
#         _u = data['uy'][i, j]
#         for k in range(0, _levels - 1):
#             for n in range(0, _levels - 1):
#
#                 if x[k + 1] >= data['x'][i] >= x[k] and y[n + 1] >= data['y'][j] >= y[n]:
#                     v_x[k, n] = _v
#                     v_y[k, n] = _u
#
# plt.quiver(x, y, v_x, v_y, v_x, headlength=5)  # print data.attrs
#
# plt.show()

# calc_staff(0)
#
# for i in range(0, files.__len__()):
#     calc_staff(i)


# import multiprocessing
#
# pool = multiprocessing.Pool(1)
#
# pool.map(calc_staff, range(0, files.__len__() -1))


import spacepy.pybats.bats

# data = spacepy.pybats.IdlBin("z=0_ful_1_t00062640_n00000100.out")
# data = file_data = FileData.FileData("z=0_ful_1_t00000000_n00000000.out")


#
# data.extract2([2,4],1, var="rho")
# for file in files:
