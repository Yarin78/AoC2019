import re
import itertools
from queue import Queue

_integer_pattern = re.compile("-?[0-9]+")

def get_ints(line):
    return [int(m) for m in _integer_pattern.findall(line)]

def chunk(s, chunk_size):
    '''Splits a string into chunks given the specified chunk size'''
    res = []
    i = 0
    while i < len(s):
        res.append(s[i:min(i+chunk_size, len(s))])
        i += chunk_size
    return res

def bfs(graph, start):
    '''Performs a BFS search in a graph and returns the distans to all nodes visited.
    graph: {node: [neighbors]}
    '''
    dist = {}  # node -> distance
    q = Queue()
    q.put(start)
    dist[start] = 0
    while not q.empty():
        current = q.get()
        steps = dist[current]
        for neighbor in graph.get(current, []):
            if neighbor not in dist:
                dist[neighbor] = steps + 1
                q.put(neighbor)
    return dist


def generate_primes(n):
    '''Generates all primes up to and include n.
    If you want to use factorize, you only need to generate to n**0.5.'''
    n = int(n)
    if n==2:
        return [2]
    elif n<2:
        return []
    s=list(range(3,n+1,2))
    mroot = n ** 0.5
    half=(n+1)//2-1
    i=0
    m=3
    while m <= mroot:
        if s[i]:
            j=(m*m-3)//2
            s[j]=0
            while j<half:
                s[j]=0
                j+=m
        i=i+1
        m=2*i+3
    return [2]+[x for x in s if x]

def factorize(n, primes=None):
    if n == 0:
        return []
    factors = []
    if not primes:
        primes=itertools.chain([2], range(2, int(n ** 0.5)+1))  # Not primes, but works
    for p in primes:
        while n % p == 0:
            n = n // p
            factors.append(p)
        if n == 1:
            break
    if n > 1:
        factors.append(n)
    return factors

if __name__ == "__main__":
    primes = None #generate_primes(1000001000**0.5)
    for i in range(1000000000,1000001000):
        print(i, factorize(i, primes))

