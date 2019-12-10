import sys
import math
from queue import Queue
from collections import defaultdict
from itertools import permutations
from lib import util
from lib.geo2d import *
from lib.intcode import *
from aocd import data, submit

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a%b)

lines = data.strip().split('\n')
map = [list(line) for line in lines]
xsize = len(lines[0])
ysize = len(lines)

total_count = 0
best = 0
for y in range(ysize):
    for x in range(xsize):
        if map[y][x] != '#':
            continue
        total_count += 1
        angles = set()
        for ty in range(ysize):
            for tx in range(xsize):
                if lines[ty][tx] != '#' or (y == ty and x == tx):
                    continue
                dx = tx-x
                dy = ty-y
                d = gcd(abs(dx), abs(dy))
                dx //= d
                dy //= d
                angles.add((dx, dy))
        if len(angles) > best:
            sx = x
            sy = y
            best = len(angles)

print(best, sx, sy)

wave = 0
asteroids = []
while len(asteroids) < total_count - 1:
    wave += 1

    angles = set()
    for ty in range(ysize):
        for tx in range(xsize):
            if map[ty][tx] != '#' or (tx == sx and ty == sy):
                continue
            dx = tx-sx
            dy = ty-sy
            d = gcd(abs(dx), abs(dy))
            dx //= d
            dy //= d
            angles.add((dx, dy))

    for (dx,dy) in angles:
        angle = math.atan2(dy,dx)
        if dy < 0 and dx < 0:
            angle += 2*math.pi
        cx = sx+dx
        cy = sy+dy
        while map[cy][cx] != '#':
            cx += dx
            cy += dy
        if map[cy][cx] == '#':
            asteroids.append((wave, angle, cx, cy))
            map[cy][cx] = '.'

asteroids.sort()
print(asteroids[199][2:])
