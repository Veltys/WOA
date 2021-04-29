# -*- coding: utf-8 -*-


from copy import copy
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


def benchark2020(x, benchmark_id):
        libtest = ctypes.CDLL(os.path.dirname(os.path.abspath(__file__)) + os.sep + 'libbenchmark.' + ('dll' if os.name == 'nt' else 'so'))
        libtest.cec20_bench.argtypes = (ctypes.c_size_t, ctypes.c_size_t, ctypes.POINTER(ctypes.c_double * x.size), ctypes.c_ushort)
        libtest.cec20_bench.restype = ctypes.c_void_p
        libtest.free_array.argtypes = (ctypes.c_void_p,)
        libtest.free_array.restype = None

        arr = libtest.cec20_bench(x.shape[0], x.shape[1], (ctypes.c_double * x.size)(*np.concatenate(np.transpose(x)).flat), benchmark_id)

        res = ctypes.cast(arr, ctypes.POINTER(ctypes.c_double * x.shape[0]))

        res = copy(res[0])

        libtest.free_array(arr)

        return res


def benchmark1(x): return benchark2020(x, 1)
def benchmark2(x): return benchark2020(x, 2)
def benchmark3(x): return benchark2020(x, 3)
def benchmark4(x): return benchark2020(x, 4)
def benchmark5(x): return benchark2020(x, 5)
def benchmark6(x): return benchark2020(x, 6)
def benchmark7(x): return benchark2020(x, 7)
def benchmark8(x): return benchark2020(x, 8)
def benchmark9(x): return benchark2020(x, 9)
def benchmark10(x): return benchark2020(x, 10)
