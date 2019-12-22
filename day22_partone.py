import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from lib.util import *
from lib.graph import *
from lib.geo2d import *
from lib.intcode import *
from aocd import data, submit
from lib.mod_prime import *


lines = data.strip().split('\n')
deck = list(range(10007))

n = len(deck)
for line in lines:
    if line == "deal into new stack":
        deck.reverse()
    elif line.startswith("cut"):
        cut = int(line[4:])
        deck = deck[cut:] + deck[:cut]
    else:
        assert line.startswith("deal with increment")
        incr = int(line[20:])
        new_deck = []
        for i in range(n):
            j = i
            while j % incr != 0:
                j += n
            new_deck.append(deck[j // incr])
        deck = new_deck

print(deck.index(2019))
