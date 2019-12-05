import sys
from collections import defaultdict
from lib import util
from queue import Queue
from lib.geo2d import *
from lib.intcode import *
from aocd import data, submit

# Make sure AOC_SESSION is updated! (Chrome inspector -> Application tab -> session)

lines = data.strip().split('\n')
#prog = intcode.Program(data)

# submit(?, part="a", day=?, year=2019)
# submit(?, part="b", day=?, year=2019)
