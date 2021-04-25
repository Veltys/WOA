# -*- coding: utf-8 -*-


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
