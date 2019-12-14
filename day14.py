import math
import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from lib.util import *
from lib.graph import *
from aocd import data, submit

lines = data.strip().split('\n')

req = {}
g = {}
for line in lines:
    line = line.replace(',', '').replace(' => ', ' ')
    parts = line.split(' ')
    p = []
    q = []

    for i in range((len(parts)-2) // 2):
        p.append((parts[i*2+1], int(parts[i*2])))
        q.append(parts[i*2+1])
    req[parts[-1]] = (int(parts[-2]), p)
    g[parts[-1]] = q

#print(g)
order = topological_sort(g)
order.reverse()

def ore_required(x):
    global order, req
    hm = defaultdict(int)
    hm['FUEL'] = x
    for output in order:
        if output == 'ORE':
            return hm[output]
        (quant, ingred) = req[output]
        a = int(math.ceil(hm[output] / quant))
        #print('need %d %s, must produce %d times receipt %s' % (hm[output], output, a, req[output]))
        for (b, c) in ingred:
            hm[b] += c*a

print(ore_required(1))

target= 1000000000000
lo = 0
hi = 10000000000
while lo < hi:
    x = (lo+hi)//2
    if ore_required(x) > 1000000000000:
        hi = x
        #print('does not work with %d' % x)
    else:
        lo = x+1
        #print('works with %d' % x)

print(lo-1)
