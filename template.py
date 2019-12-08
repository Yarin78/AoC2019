import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from lib import util
from lib.geo2d import *
from lib.intcode import *
from aocd import data, submit

# Make sure AOC_SESSION is updated! (Chrome inspector -> Application tab -> session)

lines = data.strip().split('\n')
#prog = Program(data)

# submit(?, part="a", day=?, year=2019)
# submit(?, part="b", day=?, year=2019)
