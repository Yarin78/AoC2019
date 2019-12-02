import sys
from collections import defaultdict
from lib import util
from queue import Queue
from aocd import data, submit

# Make sure AOC_SESSION is updated! (Chrome inspector -> Application tab -> session)

lines = data.strip().split('\n')

# submit(cnt, part="a", day=1, year=2019)
