__author__ = 'artem'

import TecData

file = "resources/a24900.dat"

import matplotlib.pyplot as plt

file_data = TecData.TecData(file)

figure, ax = plt.subplots()

file_data.plot_velocity_filed(ax)
plt.show()