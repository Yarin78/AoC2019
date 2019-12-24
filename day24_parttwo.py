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

empty = [".....", ".....",".....",".....","....."]

levels = [ empty[:], empty[:], lines, empty[:], empty[:]]
for minutes in range(200):
    print('minute', minutes)
    new_levels = [empty[:], empty[:]]
    num_bugs = 0
    for lvl in range(1, len(levels)-1):
        nl = []
        for y in range(5):
            s = ''
            for x in range(5):
                if x==2 and y == 2:
                    s += '.'
                    continue
                p = Point(x,y)
                cnt = 0

                for d in DIRECTIONS:
                    np = p+d
                    if np.x < 0:
                        if levels[lvl-1][2][1] == '#':
                            cnt += 1
                    elif np.x >= 5:
                        if levels[lvl-1][2][3] == '#':
                            cnt += 1
                    elif np.y < 0:
                        if levels[lvl-1][1][2] == '#':
                            cnt += 1
                    elif np.y >= 5:
                        if levels[lvl-1][3][2] == '#':
                            cnt += 1
                    elif np.y == 2 and np.x == 2:
                        if x == 1:
                            for ny in range(5):
                                if levels[lvl+1][ny][0] == '#':
                                    cnt += 1
                        elif x == 3:
                            for ny in range(5):
                                if levels[lvl+1][ny][4] == '#':
                                    cnt += 1
                        elif y == 1:
                            for nx in range(5):
                                if levels[lvl+1][0][nx] == '#':
                                    cnt += 1
                        elif y == 3:
                            for nx in range(5):
                                if levels[lvl+1][4][nx] == '#':
                                    cnt += 1
                        else:
                            assert False
                    else:
                        if levels[lvl][np.y][np.x] == '#':
                            cnt += 1

                if levels[lvl][p.y][p.x] == '#':
                    if cnt == 1:
                        s += '#'
                    else:
                        s += '.'
                else:
                    if cnt == 2 or cnt == 1:
                        s += '#'
                    else:
                        s += '.'
            num_bugs += s.count('#')

            nl.append(s)


        new_levels.append(nl)
    new_levels.append(empty[:])
    new_levels.append(empty[:])
    levels = new_levels

print(num_bugs)
