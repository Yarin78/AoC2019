import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from lib.util import *
from lib.graph import *
from lib.geo2d import *
from lib.intcode import *
from aocd import data, submit
from lib.mod_prime import *


lines = data.strip().split('\n')
n = 10007

# all operations are on the formula ax+b, represented as a tuple (a,b)

pos = 2019
for line in lines:
    if line == "deal into new stack":
        op = (-1, n-1)
    elif line.startswith("cut"):
        cut = int(line[4:])
        op = (1, -cut)
    else:
        assert line.startswith("deal with increment")
        incr = int(line[20:])
        op = (incr, 0)
    pos = (pos*op[0]+op[1]) % n

print(pos)
