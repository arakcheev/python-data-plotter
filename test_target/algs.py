import matplotlib.pyplot as plt
import time
from math import *


def one(N):
    start = time.time()
    sum = 0
    n = N
    while n <= N and n > 0:
        i = 0
        while (i < n):
            sum += 1
            i += 1
        n /= 2
    stop = time.time()
    total_time = stop - start
    # c = total_time / (2 * N * log(N))
    c = total_time / N
    print c
    return total_time, sum, c


n_array = [1000, 10000, 100000, 1000000, 2000000, 10000000, 100000000]
# n_array = [1024]
# n_array = [1024, 10000, 100000, 1000000, 2000000]
# n_array = [10, 20, 30, 40, 50,60, 70, 80 ,90]

# for n in n_array:
#     res = one(n)
#     plt.plot(log10(n), res[0], 'or')
#     # plt.plot(log10(n), 6.19452668867e-09 * 2 * n * log(n), 'xr')
#     # plt.plot(log10(n), 1.73414945602e-07 * n, '+r')
# 
# # plt.show()

print "     "


def two(N):
    start = time.time()
    summ = 0
    i = 1
    while i < N:
        j = 0
        while j < i:
            summ += 1
            j += 1
        i *= 2
    stop = time.time()
    total_time = stop - start
    c = total_time / N
    print c
    return total_time, summ, c


# for n in n_array:
#     res = two(n)
#     plt.plot(log10(n), res[0], 'xb')
#     # plt.plot(log10(n), 9.46370363235e-08 * n, '+b')
# # 
# plt.show()


b = log(17.091 / 3.659, 2)
a = 17.091 / (pow(32768, b))

print b, a

print a * pow(65536, b)
