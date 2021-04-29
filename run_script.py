#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : run_script.py
# Description   : Runner for this algorithm
# Author        : Veltys
# Date          : 2021-04-29
# Version       : 1.0.1
# Usage         : python3 run_script.py
# Notes         : Use flag -h to see optional commands and help


import argparse
import linecache
import os
import re
import sys

import numpy

import run as m


def parseClArgs(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-fMin', type = int, default = 1, dest = 'fMin', choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], help = 'minimum function id for benchmark 2020 (default: 1)')
    parser.add_argument('-fMax', type = int, default = 10, dest = 'fMax', choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], help = 'maximum function id for benchmark 2020; have to be greater or equal to fMin (default: 10)')
    parser.add_argument('-fStep', type = int, default = 1, dest = 'fStep', choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], help = 'function id step for benchmark 2020 (default: 1)')
    parser.add_argument('-dMin', type = int, default = 10, dest = 'dMin', choices = [10, 15, 20], help = 'minimum dimension (default: 10)')
    parser.add_argument('-dMax', type = int, default = 20, dest = 'dMax', choices = [10, 15, 20], help = 'maximum dimension; have to be greater or equal to dMin (default: 20)')
    parser.add_argument('-dStep', type = int, default = 5, dest = 'dStep', choices = [10, 15, 20], help = 'dimension step (default: 5)')
    parser.add_argument('-e', '--execute', default = True, dest = 'execute', action = argparse.BooleanOptionalAction, help = 'make execution phase')
    parser.add_argument('-p', '--postprocessing', default = True, dest = 'postprocessing', action = argparse.BooleanOptionalAction, help = 'make postprocessing phase')

    args = parser.parse_args(argv)

    return args


def guardar(alg, funcion, dimensiones, res):
    fileName = f'{alg}_{funcion}_{dimensiones}.txt'

    try:
        out = open(fileName, 'w')

    except IOError:
        print(f'Error de apertura del archivo <{fileName}>')
        print(f'ERROR: imposible abrir el archivo <{fileName}>', file = sys.stderr)

        exit(os.EX_OSFILE) # @UndefinedVariable

    else:
        for i in range(16):
            for j in range(30):
                out.write(str(res[i][j]))

                if j != 29:
                    out.write(',')

            # out.write(os.linesep)
            out.write("\n")

        out.close()


def posprocesar(dimensiones):
    # Recogida de todos los archivos de salida
    archivo = [ name for name in os.listdir('.') if os.path.isfile(os.path.join('.', name)) and re.match(r"^experiment-\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}.csv$", name) ]

    archivo = archivo[0]

    # Preparación de la matriz de resultados
    res = numpy.zeros((16, 30))

    for i in range(30):
        linea = linecache.getline(archivo, i * 2 + 3)

        linea = linea.split(',')

        for j in range(16):
            # Número de columna a leer
            numColumna = int(round((dimensiones ** (j / 5 - 3)) * 150000, 0))

            try: # Algunas líneas podrían no existir, debido a los criterios de parada
                elemento = linea[numColumna + 2]

            except IndexError: # En tal caso, se copia el resultado de la línea anterior
                res[j][i] = res[j - 1][i]

            else:
                res[j][i] = elemento

    os.remove(archivo)

    return res


def main(argv):
    # Preprocesamiento: variables

    alg = 'WOA'

    args = parseClArgs(argv)

    for i in range(args.fMin - args.fStep, args.fMax, args.fStep):
        for j in range(args.dMin - args.dStep, args.dMax, args.dStep):
            if(args.execute):
                # Procesamiento: ejecución del programa
                print(f'Función {i + args.fStep}, dimensión {j + args.dStep}')

                m.main(['-func', 'benchmark' + str(i + args.fStep), '-d', str(j + args.dStep)])

            if(args.postprocessing):
                # Posprocesamiento: recopilación de resultados
                guardar(alg, i + args.fStep, j + args.dStep, posprocesar(j + args.dStep))


if __name__ == '__main__':
    main(sys.argv[1:])

