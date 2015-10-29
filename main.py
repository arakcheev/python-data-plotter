__author__ = 'artem'

import glob
import FileData
import Parameters
import matplotlib.pyplot as plt

files = glob.glob("/Users/artem/workspace/kiae/swmf_mag2/run/GM/IO2/*.out")

# outFiles = glob.glob("srez/*.png")
n = 0
totalFiles = float(files.__len__())

for file in files:
    n += 1
    print "Plot file (" + "{0:.2f}".format(n / totalFiles * 100) + "%) " + str(file)
    filedata = FileData.FileData(file)
    # figure, ax = plt.subplots()
    # filedata.plotContour(ax)
    # filedata.plotRocheLobe(ax)
    # filedata.plotVelocityFiled(ax)
    figure = filedata.srez()
    figure.suptitle('T=7500, time = ' + str(filedata.time / Parameters.Parameters.period))

    plt.savefig('/Users/artem/workspace/inasan/SWMF/data/7500/srez/srez_' + str(
        filedata.fileNumber) + '.png')
    plt.close(figure)
