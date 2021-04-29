import numpy as np


class WhaleOptimization():
    """class implements the whale optimization algorithm as found at
    http://www.alimirjalili.com/WOA.html
    and
    https://doi.org/10.1016/j.advengsoft.2016.01.008
    """
    def __init__(self, optFunc, constraints, nsols, b, a, aStep, maximize = False):
        self._optFunc = optFunc
        self._constraints = constraints
        self._sols = self._initSolutions(nsols)
        self._b = b
        self._a = a
        self._aStep = aStep
        self._maximize = maximize
        self._bestSolutions = []


    def getSolutions(self):
        """return solutions"""
        return self._sols


    def getBestSolutions(self):
        return [ s[0] for s in self._bestSolutions ]


    def optimize(self):
        """solutions randomly encircle, search or attack"""
        rankedSol = self._rankSolutions()
        bestSol = rankedSol[0]
        # include best solution in next generation solutions
        newSols = [bestSol]

        for s in rankedSol[1:]:
            if np.random.uniform(0.0, 1.0) > 0.5:
                a = self._computeA()
                normA = np.linalg.norm(a)
                if normA < 1.0:
                    newS = self._encircle(s, bestSol, a)
                else:
                    # ##select random sol
                    randomSol = self._sols[np.random.randint(self._sols.shape[0])]
                    newS = self._search(s, randomSol, a)
            else:
                newS = self._attack(s, bestSol)
            newSols.append(self._constrain_solution(newS))

        self._sols = np.stack(newSols)
        self._a -= self._aStep


    def _initSolutions(self, nsols):
        """initialize solutions uniform randomly in space"""
        sols = []
        for c in self._constraints:
            sols.append(np.random.uniform(c[0], c[1], size = nsols))

        sols = np.stack(sols, axis = -1)
        return sols


    def _constrain_solution(self, sol):
        """ensure solutions are valid wrt to constraints"""
        constrainS = []
        for c, s in zip(self._constraints, sol):
            if c[0] > s:
                s = c[0]
            elif c[1] < s:
                s = c[1]
            constrainS.append(s)
        return constrainS


    def _rankSolutions(self):
        """find best solution"""

        if len(self._constraints) == 2:
            fitness = self._optFunc(self._sols[:, 0], self._sols[:, 1])
        else:
            fitness = self._optFunc(self._sols)

        solFitness = [(f, s) for f, s in zip(fitness, self._sols)]

        # best solution is at the front of the list
        rankedSol = list(sorted(solFitness, key = lambda x:x[0], reverse = self._maximize))
        self._bestSolutions.append(rankedSol[0])

        return [s[1] for s in rankedSol]


    def printBestSolutions(self):
        print('generation best solution history')
        print('([fitness], [solution])')
        for s in self._bestSolutions:
            print(s)
        print('\n')
        print('best solution')
        print('([fitness], [solution])')
        print(sorted(self._bestSolutions, key = lambda x:x[0], reverse = self._maximize)[0])


    def _computeA(self):
        r = np.random.uniform(0.0, 1.0, size = len(self._constraints))
        return (2.0 * np.multiply(self._a, r)) - self._a


    def _computeC(self):
        return 2.0 * np.random.uniform(0.0, 1.0, size = len(self._constraints))


    def _encircle(self, sol, bestSol, a):
        d = self._encircleD(sol, bestSol)
        return bestSol - np.multiply(a, d)


    def _encircleD(self, sol, bestSol):
        c = self._computeC()
        d = np.linalg.norm(np.multiply(c, bestSol) - sol)
        return d


    def _search(self, sol, randSol, a):
        d = self._searchD(sol, randSol)
        return randSol - np.multiply(a, d)


    def _searchD(self, sol, randSol):
        c = self._computeC()
        return np.linalg.norm(np.multiply(c, randSol) - sol)


    def _attack(self, sol, bestSol):
        d = np.linalg.norm(bestSol - sol)
        l = np.random.uniform(-1.0, 1.0, size = len(self._constraints))
        return np.multiply(np.multiply(d, np.exp(self._b * l)), np.cos(2.0 * np.pi * l)) + bestSol
