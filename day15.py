import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from lib.util import *
from lib.graph import *
from lib.geo2d import *
from lib.intcode import *
from aocd import data, submit

lines = data.strip().split('\n')
prog = Program(data)

map = {}
goal = None

DIRS = [NORTH, SOUTH, WEST, EAST]
OPP_DIR = [1,0,3,2]

input_queue = Queue()

def search(pos):
    global map,goal,prog
    map[pos] = '.'
    for dir in range(4):
        new_pos = pos+DIRS[dir]
        if new_pos not in map:
            input_queue.put(dir+1)
            status = prog.run_until_next_io(input_queue)

            if status:
                if status == 2:
                    goal = new_pos
                search(new_pos)
                input_queue.put(OPP_DIR[dir]+1)
                status = prog.run_until_next_io()
                assert status != 0
            else:
                map[new_pos] = '#'


search(Point(0,0))
map[Point(0,0)] = 'S'
map[goal] = 'G'

print_array(gridify_sparse_map(map))

g = {}
for p, c in map.items():
    if c in '.GS':
        neighbors = []
        for d in DIRS:
            if map[p + d] in '.GS':
                neighbors.append(p+d)
        g[p] = neighbors

dist = bfs(g, Point(0,0))

print(dist[goal])

dist = bfs(g, goal)

print(max(dist.values()))
