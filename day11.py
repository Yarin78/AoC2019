import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from lib import util
from lib.graph import *
from lib.geo2d import *
from lib.intcode import *
from aocd import data, submit

lines = data.strip().split('\n')
prog = Program(data)

DIRECTIONS = [NORTH, EAST, SOUTH, WEST]

class Reader:
    def get(self):
        global dir, pos, map
        return map[pos]

    def get_nowait(self):
        return self.get()

class Writer:
    def __init__(self):
        self.p = 0

    def put(self, v):
        global dir, pos, map
        if self.p == 0:
            map[pos] = v
            self.p = 1
        elif self.p == 1:
            if v == 0:
                dir = (dir+3)%4
            else:
                dir = (dir+1)%4
            pos += DIRECTIONS[dir]
            self.p = 0

# Star 1
pos=Point(0,0)
dir=0

map = defaultdict(int)

prog.run(Reader(), Writer())

print(len(map))

# Star 2
pos=Point(0,0)
dir=0

map = defaultdict(int)
map[Point(0,0)] = 1

prog.reset()
prog.run(Reader(), Writer())

minx = min(p.x for p in map.keys())
miny = min(p.y for p in map.keys())
maxx = max(p.x for p in map.keys())
maxy = max(p.y for p in map.keys())

for y in range(miny, maxy+1):
    print(''.join(['#' if map[Point(x,y)] else '.' for x in range(minx, maxx+1)]))
