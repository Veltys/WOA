import argparse
import sys

import numpy as np

from src.animate_scatter import AnimateScatter
from src.whale_optimization import WhaleOptimization


def parseClArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-nsols", type = int, default = 50, dest = 'nsols', help = 'number of solutions per generation, default: 50')
    parser.add_argument("-ngens", type = int, default = 30, dest = 'ngens', help = 'number of generations, default: 20')
    parser.add_argument("-a", type = float, default = 2.0, dest = 'a', help = 'woa algorithm specific parameter, controls search spread default: 2.0')
    parser.add_argument("-b", type = float, default = 0.5, dest = 'b', help = 'woa algorithm specific parameter, controls spiral, default: 0.5')
    parser.add_argument("-c", type = float, default = None, dest = 'c', help = 'absolute solution constraint value, default: None, will use default constraints')
    parser.add_argument("-func", type = str, default = 'booth', dest = 'func', help = 'function to be optimized, default: booth; options: matyas, cross, eggholder, schaffer, booth')
    parser.add_argument("-r", type = float, default = 0.25, dest = 'r', help = 'resolution of function meshgrid, default: 0.25')
    parser.add_argument("-t", type = float, default = 0.1, dest = 't', help = 'animate sleep time, lower values increase animation speed, default: 0.1')
    parser.add_argument("-max", default = False, dest = 'max', action = 'store_true', help = 'enable for maximization, default: False (minimization)')

    args = parser.parse_args()
    return args


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


def main(argv): # @UnusedVariable
    args = parseClArgs()

    nSols = args.nsols
    nGens = args.ngens

    funcs = { 'schaffer': schaffer, 'eggholder': eggholder, 'booth': booth, 'matyas': matyas, 'cross': crossInTray, 'levi': levi }
    funcConstraints = { 'schaffer': 100.0, 'eggholder': 512.0, 'booth': 10.0, 'matyas': 10.0, 'cross': 10.0, 'levi': 10.0 }

    if args.func in funcs:
        func = funcs[args.func]
    else:
        print('Missing supplied function ' + args.func + ' definition. Ensure function defintion exists or use command line options.')
        return

    if args.c is None:
        if args.func in funcConstraints:
            args.c = funcConstraints[args.func]
        else:
            print('Missing constraints for supplied function ' + args.func + '. Define constraints before use or supply via command line.')
            return

    c = args.c
    constraints = [[-c, c], [-c, c]]

    optFunc = func

    b = args.b
    a = args.a
    aStep = a / nGens

    maximize = args.max

    optAlg = WhaleOptimization(optFunc, constraints, nSols, b, a, aStep, maximize)
    solutions = optAlg.getSolutions()
    colors = [[1.0, 1.0, 1.0] for _ in range(nSols)]

    aScatter = AnimateScatter(constraints[0][0],
                               constraints[0][1],
                               constraints[1][0],
                               constraints[1][1],
                               solutions, colors, optFunc, args.r, args.t)

    for _ in range(nGens):
        optAlg.optimize()
        solutions = optAlg.getSolutions()
        aScatter.update(solutions)

    optAlg.printBestSolutions()


if __name__ == '__main__':
    main(sys.argv[1:])
