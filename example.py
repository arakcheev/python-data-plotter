import matplotlib

matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import numpy as np
import struct

path = '/media/artem/Storage/Mdot/Line0/a105000.bin'

# 1) Open file here
file = open(path, 'rb')

# Read header number first. Number is 4 bytes integer number.
header = struct.unpack("i", file.read(4))
print header[0]

# Read timer bytes
timerString = file.read(header[0])
print timerString
# Unpack timer bytes to numbers: Counter and time from begging of simulation
counter, timer = struct.unpack("ld", file.read(16))
print counter
print timer

# Read grid tag
gridTag = struct.unpack("i", file.read(4))[0]
print gridTag

# Read grid bytes.
gridString = file.read(gridTag)
print gridString
# Unpack greed bytes to number - grid dimension
dim = struct.unpack("i", file.read(4))[0]
print dim

# Then unpack 6 dimensions from read bytes
xmin, xmax, ymin, ymax, zmin, zmax = struct.unpack("dddddd", file.read(6 * 8))
print xmin, xmax, ymin, ymax, zmin, zmax

# Read and unpack ghos cells. Number of ghost cells
gl = struct.unpack("i", file.read(4))[0]
print gl

# Read and unpack grid cells
nx, ny, nz = struct.unpack("lll", file.read(3 * 8))
print nx, ny, nz

# Read grid. (grid cells) + (ghost cells)* 2 + 1
# 28.82 here - dimension units
X = np.fromfile(file, np.dtype("d"), (nx + 2 * gl + 1)) * 28.82
Y = np.fromfile(file, np.dtype("d"), (ny + 2 * gl + 1)) * 28.82
Z = np.fromfile(file, np.dtype("d"), (nz + 2 * gl + 1)) * 28.82

# Read array tag
arrayTag = file.read(struct.unpack("i", file.read(4))[0])
print arrayTag

# Read data count values.
dataCount = struct.unpack("i", file.read(4))[0]
print dataCount

# read main array of data
# Data - matrix in form of single array with dimentions  nz * ny * nx * dataCount
arr = np.fromfile(file, np.dtype("d"), nz * ny * nx * dataCount)
file.close()

# Plot data here

# arr - is single array of numbers. Reshape it to matrix and transpose.
arr = arr.reshape((nz, ny, nx, dataCount))
arr = arr.T

# Get slice of rho (zero index) as matrix
rho = np.log(arr[0][:][:].T[nz / 2 + 2])

var_min = rho.min()
var_max = rho.max()

steps = np.abs(np.abs(var_max) - np.abs(var_min)) / 40.0

levels = np.arange(var_min, var_max, steps)

fig, axes = plt.subplots()

# plot with exclude ghost cells
axes.pcolormesh(X[2:nx + 2], Y[2:ny + 2], rho, cmap="gray_r", vmin=var_min, vmax=var_max)

# set limits to axis
axes.set_ylim([-16, 16])
axes.set_xlim([-16, 16])

plt.show()
