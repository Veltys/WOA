# -*- coding: utf-8 -*-


import ctypes
import os

import numpy as np


# optimization functions from https://en.wikipedia.org/wiki/Test_functions_for_optimization


def schaffer(x, y):
    """constraints=100, minimum f(0,0)=0"""
    numer = np.square(np.sin(x ** 2 - y ** 2)) - 0.5
    denom = np.square(1.0 + (0.001 * (x ** 2 + y ** 2)))

    return 0.5 + (numer * (1.0 / denom))


def eggholder(x, y):
    """constraints=512, minimum f(512, 414.2319)=-959.6407"""
    y = y + 47.0
    a = (-1.0) * (y) * np.sin(np.sqrt(np.absolute((x / 2.0) + y)))
    b = (-1.0) * x * np.sin(np.sqrt(np.absolute(x - y)))
    return a + b


def booth(x, y):
    """constraints=10, minimum f(1, 3)=0"""
    return ((x) + (2.0 * y) - 7.0) ** 2 + ((2.0 * x) + (y) - 5.0) ** 2


def matyas(x, y):
    """constraints=10, minimum f(0, 0)=0"""
    return (0.26 * (x ** 2 + y ** 2)) - (0.48 * x * y)


def crossInTray(x, y):
    """constraints=10,
    minimum f(1.34941, -1.34941)=-2.06261
    minimum f(1.34941, 1.34941)=-2.06261
    minimum f(-1.34941, 1.34941)=-2.06261
    minimum f(-1.34941, -1.34941)=-2.06261
    """
    B = np.exp(np.absolute(100.0 - (np.sqrt(x ** 2 + y ** 2) / np.pi)))
    A = np.absolute(np.sin(x) * np.sin(y) * B) + 1
    return -0.0001 * (A ** 0.1)


def levi(x, y):
    """constraints=10,
    minimum f(1,1)=0.0
    """
    a = np.sin(3.0 * np.pi * x) ** 2
    b = ((x - 1) ** 2) * (1 + np.sin(3.0 * np.pi * y) ** 2)
    c = ((y - 1) ** 2) * (1 + np.sin(2.0 * np.pi * y) ** 2)
    return a + b + c


def rebuild(x, y):
    z = []

    for i, _ in enumerate(x):
        z.append([x[i], y[i]])

    z = np.array(z)

    return z.flatten()


def benchark2020(x):
    libtest = ctypes.CDLL(os.path.dirname(os.path.abspath(__file__)) + os.sep + '..' + os.sep + 'libbenchmark.' + ('dll' if os.name == 'nt' else 'so'))
    libtest.cec20_bench.argtypes = (ctypes.c_size_t, ctypes.c_size_t, ctypes.POINTER(ctypes.c_double * len(x)), ctypes.c_ushort)
    libtest.cec20_bench.restype = ctypes.c_double

    return libtest


def benchmark1(x, y):
    z = rebuild(x, y)

    return benchark2020(z).cec20_bench(z.size, 2, (ctypes.c_double * len(z))(*z), 1)


def benchmark2(x, y):
    z = rebuild(x, y)

    return benchark2020(z).cec20_bench(z.size, 2, (ctypes.c_double * len(z))(*z), 2)


def benchmark3(x, y):
    z = rebuild(x, y)

    return benchark2020(z).cec20_bench(z.size, 2, (ctypes.c_double * len(z))(*z), 3)


def benchmark4(x, y):
    z = rebuild(x, y)

    return benchark2020(z).cec20_bench(z.size, 2, (ctypes.c_double * len(z))(*z), 4)


def benchmark5(x, y):
    z = rebuild(x, y)

    return benchark2020(z).cec20_bench(z.size, 2, (ctypes.c_double * len(z))(*z), 5)


def benchmark6(x, y):
    z = rebuild(x, y)

    return benchark2020(z).cec20_bench(z.size, 2, (ctypes.c_double * len(z))(*z), 6)


def benchmark7(x, y):
    z = rebuild(x, y)

    return benchark2020(z).cec20_bench(z.size, 2, (ctypes.c_double * len(z))(*z), 7)


def benchmark8(x, y):
    z = rebuild(x, y)

    return benchark2020(z).cec20_bench(z.size, 2, (ctypes.c_double * len(z))(*z), 8)


def benchmark9(x, y):
    z = rebuild(x, y)

    return benchark2020(z).cec20_bench(z.size, 2, (ctypes.c_double * len(z))(*z), 9)


def benchmark10(x, y):
    z = rebuild(x, y)

    return benchark2020(z).cec20_bench(z.size, 2, (ctypes.c_double * len(z))(*z), 10)
