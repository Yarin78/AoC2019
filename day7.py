import sys
from collections import defaultdict
from lib import util
from queue import Queue
from lib.geo2d import *
from lib.intcode import *
from aocd import data, submit
from itertools import permutations

prog = [Program(data.strip(), i) for i in range(5)]

for part in range(2):
    best = 0
    for perm in permutations(range(5*part, 5*part+5)):
        pipes = [Queue() for p in prog]
        for i in range(5):
            prog[i].reset()
            prog[i].init_io(pipes[i], pipes[(i+1)%5])
            pipes[i].put(perm[i])
        pipes[0].put(0)
        parallel_executor(prog)

        best = max(best, prog[4].last_out)

    print(best)
