import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from lib import util
from lib.graph import *
from lib.geo3d import *
from lib.intcode import *
from aocd import data, submit

lines = data.strip().split('\n')
#prog = Program(data)
moon_pos = [Point(16,-8,13), Point(4,10,10), Point(17,-5,6), Point(13,-3,0)]
moon_vel = [Point(0,0,0), Point(0,0,0), Point(0,0,0), Point(0,0,0)]

mp = [[] for i in range(4)]
mv = [[] for i in range(4)]

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a%b)

def lcm(a, b):
    return a * b // gcd(a,b)

reps = []
for coord in range(3):
    if coord == 0:
        pos = [p.x for p in moon_pos]
        vel = [p.x for p in moon_vel]
    elif coord == 1:
        pos = [p.y for p in moon_pos]
        vel = [p.y for p in moon_vel]
    else:
        pos = [p.z for p in moon_pos]
        vel = [p.z for p in moon_vel]


    t = 0
    seen = {}
    while True:
        state = (pos[0], pos[1], pos[2], pos[3], vel[0], vel[1], vel[2], vel[3])
        if state in seen:
            rep = t-seen[state]
            break
        seen[state] = t
        t += 1
        for p1 in range(4):
            for p2 in range(4):
                if p1 < p2:
                    dx = pos[p1]-pos[p2]

                    if dx < 0:
                        vel[p1] += 1
                        vel[p2] -= 1
                    elif dx > 0:
                        vel[p1] -= 1
                        vel[p2] += 1

        for p in range(4):
            pos[p] += vel[p]
        if t == 1000:
            for p in range(4):
                mp[p].append(pos[p])
                mv[p].append(vel[p])

    print('repeats after %d' % rep)
    reps.append(rep)


def en(moon):
    return abs(moon[0])+abs(moon[1])+abs(moon[2])

e = 0
for p in range(4):
    e += en(mp[p]) * en(mv[p])

print(e)

print(lcm(lcm(reps[0], reps[1]), reps[2]))
