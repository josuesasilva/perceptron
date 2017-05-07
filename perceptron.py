#!/usr/bin/python2.7

from random import choice
from math import pow
from numpy import array, dot, random
from itertools import product, ifilter
from enum import Enum
import sys


class Data(Enum):
    OR = 1
    AND = 2
    XOR = 3

def get_data(size):
    if size == 2:
        return product([0, 1], [0, 1])
    elif size == 3:
        return product([0, 1], [0, 1], [0, 1])
    elif size == 4:
        return product([0, 1], [0, 1], [0, 1], [0, 1])
    elif size == 5:
        return product([0, 1], [0, 1], [0, 1], [0, 1], [0, 1])

def generate_data(size, type):
    generator = None
    result = []

    for i in get_data(size):
        data = [x for x in i]
        expected = None

        if type == Data.AND:

            if len([j for j in ifilter(lambda x: x == 0, data)]) == 0:
                expected = 1
            else:
                expected = 0

        elif type == Data.OR:

            if len([j for j in ifilter(lambda x: x == 1, data)]) > 0:
                expected = 1
            else:
                expected = 0

        elif type == Data.XOR:
            xor = None
            for j in range(len(data)):
                if j == 0:
                    continue
                else:
                    if xor == None:
                        xor = data[j-1] != data[j]
                    else:
                        xor = data[j] != xor

            if xor == True:
                expected = 1
            else:
                expected = 0

        data.append(1) # add bias

        result.append((array(data), expected))

    return result


class Perceptron:

    def __init__(self, name, data):
        self.training_data = data
        self.w = []
        self.errors = []
        self.eta = 0.3
        self.n = 100

    def _fill_weight(self):
        self.w = random.rand(len(self.training_data[0][0]))

    def _threshold(self, input):
        if input < 0:
            return 0
        else:
            return 1

    def train(self):
        self._fill_weight()

        for i in range(self.n):
            for data in self.training_data:
                x, expected = data
                result = dot(self.w, x)
                error = expected - self._threshold(result)
                self.errors.append(error)
                self.w += self.eta * error * x

        for x, i in self.training_data:
            result = dot(x, self.w)
            print("{}: {} -> {}, expected: {}".format(x[:len(x) - 1], result, self._threshold(result), i))

if __name__ == "__main__":
    training_data = generate_data(2, Data.AND)
    p = Perceptron("OR", training_data)
    p.train()

    from pylab import plot, ylim, show
    ylim([-1,1])
    plot(p.errors)
    show()
