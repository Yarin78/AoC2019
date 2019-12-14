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
    parts = intify(tokenize(line))
    parts = pair_up(parts)
    deps, (target_quant, target) = parts[0:-1], parts[-1]

    req[target] = (target_quant, deps)
    g[target] = [dep[1] for dep in deps]

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
        for (c, b) in ingred:
            hm[b] += c*a

print(ore_required(1))

target = 1000000000000
lo = 0
hi = target
while lo < hi:
    x = (lo+hi)//2
    if ore_required(x) > target:
        hi = x
    else:
        lo = x+1

print(lo-1)
