import sys
from collections import defaultdict
from lib import util, intcode
from queue import Queue
from aocd import data, submit

# Make sure AOC_SESSION is updated! (Chrome inspector -> Application tab -> session)

lines = data.strip().split('\n')
#prog = intcode.Program(data)

# submit(?, part="a", day=?, year=2019)
# submit(?, part="b", day=?, year=2019)
