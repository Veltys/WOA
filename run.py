#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import sys

from src.animate_scatter import AnimateScatter
import src.funcs
from src.whale_optimization import WhaleOptimization


def parseClArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-nsols", type = int, default = 50, dest = 'nSols', help = 'number of solutions per generation, default: 50')
    parser.add_argument("-ngens", type = int, default = 30, dest = 'nGens', help = 'number of generations, default: 30')
    parser.add_argument("-a", type = float, default = 2.0, dest = 'a', help = 'woa algorithm specific parameter, controls search spread default: 2.0')
    parser.add_argument("-b", type = float, default = 0.5, dest = 'b', help = 'woa algorithm specific parameter, controls spiral, default: 0.5')
    parser.add_argument("-c", type = float, default = None, dest = 'c', help = 'absolute solution constraint value, default: None, will use default constraints')
    parser.add_argument("-func", type = str, default = 'booth', dest = 'func', help = 'function to be optimized, default: booth; options: matyas, cross, eggholder, schaffer, booth')
    parser.add_argument("-r", type = float, default = 0.25, dest = 'r', help = 'resolution of function meshgrid, default: 0.25')
    parser.add_argument("-t", type = float, default = 0.1, dest = 't', help = 'animate sleep time, lower values increase animation speed, default: 0.1')
    parser.add_argument("-max", default = False, dest = 'max', action = 'store_true', help = 'enable for maximization, default: False (minimization)')

    args = parser.parse_args()

    return args


def main(argv): # @UnusedVariable
    args = parseClArgs()

    funcs = { 'schaffer': src.funcs.schaffer, 'eggholder': src.funcs.eggholder, 'booth': src.funcs.booth, 'matyas': src.funcs.matyas, 'cross': src.funcs.crossInTray, 'levi': src.funcs.levi }
    funcConstraints = { 'schaffer': 100.0, 'eggholder': 512.0, 'booth': 10.0, 'matyas': 10.0, 'cross': 10.0, 'levi': 10.0 }

    if args.func in funcs:
        optFunc = funcs[args.func]
    else:
        print('Missing supplied function ' + args.func + ' definition. Ensure function defintion exists or use command line options.')
        return

    if args.c is None:
        if args.func in funcConstraints:
            args.c = funcConstraints[args.func]
        else:
            print('Missing constraints for supplied function ' + args.func + '. Define constraints before use or supply via command line.')
            return

    constraints = [[-args.c, args.c], [-args.c, args.c]]

    b = args.b
    a = args.a
    aStep = a / args.nGens

    optAlg = WhaleOptimization(optFunc, constraints, args.nSols, b, a, aStep, args.max)
    solutions = optAlg.getSolutions()
    colors = [[1.0, 1.0, 1.0] for _ in range(args.nSols)]

    aScatter = AnimateScatter(constraints[0][0],
                               constraints[0][1],
                               constraints[1][0],
                               constraints[1][1],
                               solutions, colors, optFunc, args.r, args.t)

    for _ in range(args.nGens):
        optAlg.optimize()
        solutions = optAlg.getSolutions()
        aScatter.update(solutions)

    optAlg.printBestSolutions()


if __name__ == '__main__':
    main(sys.argv[1:])
