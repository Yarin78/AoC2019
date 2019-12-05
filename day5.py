import sys
from collections import defaultdict
from lib import util
from queue import Queue
from lib.geo2d import *
from lib.intcode import Program
from aocd import data, submit

# Make sure AOC_SESSION is updated! (Chrome inspector -> Application tab -> session)

#lines = data.strip().split('\n')
prog = Program(data)

# submit(?, part="a", day=5, year=2019)
# submit(?, part="b", day=5, year=2019)
#prog.log_info()
#prog.show(0)

prog.run(input=[5])
