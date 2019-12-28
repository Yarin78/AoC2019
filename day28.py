import sys
import random
from queue import Queue
from collections import defaultdict
from itertools import permutations
from lib.util import *
from lib.graph import *
from lib.geo2d import *
from lib.intcode import *

data = sys.stdin.readline()

prog = Program(data)
#prog.log_info()
prog.init_io(Queue(), Queue())
print('Size: %d' % len(prog.mem))
#prog.show(0)
#exit(0)

max_instr = 0
for i in range(100):
    a = random.randrange(0, 2**64)
    b = random.randrange(1, a+1)
    prog.reset()
    res = prog.run_until_next_io(feed_input=[a,b])
    if prog.count > max_instr:
        max_instr=prog.count
    assert res == a//b, '%d/%d = %d, expected %d' % (a, b, res, a//b)

print(max_instr)
