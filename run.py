#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import csv
import errno
from itertools import chain
import os
from re import match
import sys
import time

import progressbar

# from src.animate_scatter import AnimateScatter
import src.funcs
from src.whale_optimization import WhaleOptimization


def parseClArgs(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-nsols', type = int, default = 50, dest = 'nSols', help = 'number of solutions per generation, default: 50')
    parser.add_argument('-ngens', type = int, default = 150000, dest = 'nGens', help = 'number of generations, default: 150000')
    parser.add_argument('-a', type = float, default = 2.0, dest = 'a', help = 'woa algorithm specific parameter, controls search spread default: 2.0')
    parser.add_argument('-b', type = float, default = 0.5, dest = 'b', help = 'woa algorithm specific parameter, controls spiral, default: 0.5')
    parser.add_argument('-c', type = float, default = None, dest = 'c', help = 'absolute solution constraint value, default: None, will use default constraints')
    parser.add_argument('-func', type = str, default = 'booth', dest = 'func', choices = ['matyas', 'cross', 'eggholder', 'schaffer', 'booth', 'benchmark1', 'benchmark2', 'benchmark3', 'benchmark4', 'benchmark5', 'benchmark6', 'benchmark7', 'benchmark8', 'benchmark9', 'benchmark10'], help = 'function to be optimized, default: booth')
    parser.add_argument('-r', type = float, default = 0.25, dest = 'r', help = 'resolution of function meshgrid, default: 0.25')
    # parser.add_argument('-t', type = float, default = 0.1, dest = 't', help = 'animate sleep time, lower values increase animation speed, default: 0.1')
    parser.add_argument('-max', default = False, dest = 'max', action = 'store_true', help = 'enable for maximization, default: False (minimization)')
    parser.add_argument('-e', '--maxEvals', type = int, default = 500000, dest = 'maxEvals', help = 'maximum evaluations, default: 500.000')
    parser.add_argument('-nRuns', type = int, default = 30, dest = 'nRuns', help = 'number of runs, default: 30')
    parser.add_argument('-v', '--verbose', default = False, dest = 'verbose', action = 'store_true', help = 'enable for verbosity, default: False (no verbose)')
    parser.add_argument('-x', '--export', default = True, dest = 'export', action = 'store_false', help = 'enable for prevent exporting data to CSV')
    parser.add_argument('-d', type = int, default = 10, dest = 'dim', help = 'dimensions for external benchmarks family, default: 10')
    parser.add_argument('-p', '--progress', default = True, dest = 'progress', action = 'store_false', help = 'don\'t show progress bar')


    args = parser.parse_args(argv)

    return args


def woa(args, optFunc, csvOut):
    optimizer = 'WOA'

    if match(r"^benchmark\d{1,2}$", args.func):
        constraints = []

        for _ in range(args.dim):
            constraints.append([-args.c, args.c])
    else:
        constraints = [[-args.c, args.c], [-args.c, args.c]]

    b = args.b
    a = args.a
    aStep = a / args.nGens

    if args.verbose:
        print(f'{optimizer} is optimizing with {optFunc.__name__}')

    for _ in range(args.nRuns):
        if args.progress:
            pb = progressbar.ProgressBar(max_value=args.maxEvals)

        evals = 0

        if args.progress:
            pb.update(evals)

        timerStart = time.time()

        optAlg = WhaleOptimization(optFunc, constraints, args.nSols, b, a, aStep, args.max)

        # solutions = optAlg.getSolutions()

        # colors = [[1.0, 1.0, 1.0] for _ in range(args.nSols)]

        '''

    aScatter = AnimateScatter(constraints[0][0],

                               constraints[0][1],

                               constraints[1][0],

                               constraints[1][1],

                               solutions, colors, optFunc, args.r, args.t)

    '''

        for _ in range(args.nGens):
            optAlg.optimize()

            # solutions = optAlg.getSolutions()

            # aScatter.update(solutions)

            evals += args.nSols

            if args.progress:
                pb.update(evals)

            if evals >= args.maxEvals:
                if args.progress:
                    # pb.update(evals)
                    pb.finish()

                break

        if args.progress:
            pb.finish()

        timerEnd = time.time()

        if args.verbose:
            # optAlg.printBestSolutions()
            print(f'Best solutions: {optAlg.getBestSolutions()}\n\n')

        if args.export:
            csvOut.writerow(chain.from_iterable([[optimizer, optFunc.__name__, timerEnd - timerStart], optAlg.getBestSolutions()]))


def main(argv): # @UnusedVariable
    NOMBRE_ARCHIVO = f'experiment-{time.strftime("%Y-%m-%d-%H-%M-%S")}.csv'

    args = parseClArgs(argv)

    funcs = {
        'schaffer': src.funcs.schaffer,
        'eggholder': src.funcs.eggholder,
        'booth': src.funcs.booth,
        'matyas': src.funcs.matyas,
        'cross': src.funcs.crossInTray,
        'levi': src.funcs.levi,
        'benchmark1': src.funcs.benchmark1,
        'benchmark2': src.funcs.benchmark2,
        'benchmark3': src.funcs.benchmark3,
        'benchmark4': src.funcs.benchmark4,
        'benchmark5': src.funcs.benchmark5,
        'benchmark6': src.funcs.benchmark6,
        'benchmark7': src.funcs.benchmark7,
        'benchmark8': src.funcs.benchmark8,
        'benchmark9': src.funcs.benchmark9,
        'benchmark10': src.funcs.benchmark10,
    }

    funcConstraints = {
        'schaffer': 100.0,
        'eggholder': 512.0,
        'booth': 10.0,
        'matyas': 10.0,
        'cross': 10.0,
        'levi': 10.0,
        'benchmark1': 100,
        'benchmark2': 100,
        'benchmark3': 100,
        'benchmark4': 100,
        'benchmark5': 100,
        'benchmark6': 100,
        'benchmark7': 100,
        'benchmark8': 100,
        'benchmark9': 100,
        'benchmark10': 100,
    }

    if args.func in funcs:
        optFunc = funcs[args.func]
    else:
        print('Missing supplied function ' + args.func + ' definition. Ensure function defintion exists or use command line options.')

        sys.exit(errno.EPERM)

    if args.c is None:
        if args.func in funcConstraints:
            args.c = funcConstraints[args.func]
        else:
            print('Missing constraints for supplied function ' + args.func + '. Define constraints before use or supply via command line.')

            sys.exit(errno.EPERM)

    try:
        if args.export:
            out = open(f'.{os.sep}{NOMBRE_ARCHIVO}', 'a')

    except IOError:
        print(f'Error de apertura del archivo <{NOMBRE_ARCHIVO}>')
        print(f'ERROR: imposible abrir el archivo <{NOMBRE_ARCHIVO}>', file = sys.stderr)

        sys.exit(errno.EIO)

    else:
        if args.export:
            # CSV file header
            header = []

            for i in range(args.nGens):
                header.append(f'It{i + 1}')

            csvOut = csv.writer(out, delimiter = ',')
            csvOut.writerow(chain.from_iterable([['Optimizer', 'objfname', 'ExecutionTime'], header]))

        woa(args, optFunc, csvOut)

        if args.export:
            out.close()

        if args.progress:
            print()


if __name__ == '__main__':
    main(sys.argv[1:])
