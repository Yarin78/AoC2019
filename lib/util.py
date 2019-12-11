import re
import itertools
from lib.geo2d import Point

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

def gridify_sparse_map(map, output_func=None):
    '''Converts a map of dict(Point) or dict((x,y)) into an array of strings. Determines min and max coordinates used.'''
    if isinstance(next(iter(map.keys())), Point):
        get_x = lambda p: p.x
        get_y = lambda p: p.y
        get_p = lambda x, y: Point(x,y)
    else:
        get_x = lambda p: p[0]
        get_y = lambda p: p[1]
        get_p = lambda x, y: (x,y)

    minx = min(get_x(p) for p in map.keys())
    miny = min(get_y(p) for p in map.keys())
    maxx = max(get_x(p) for p in map.keys())
    maxy = max(get_y(p) for p in map.keys())

    res = []
    for y in range(miny, maxy+1):
        s = ''
        for x in range(minx, maxx+1):
            p = get_p(x,y)
            c = map[p] if p in map else None
            if output_func:
                s += output_func(c)
            else:
                s += str(c) if c else '.'
        res.append(s)
    return res

def print_array(array):
    for a in array:
        print(a)

if __name__ == "__main__":
    #primes = generate_primes(1000001000**0.5)
    #for i in range(1000000000,1000001000):
    #    print(i, factorize(i, primes))


    print_array(gridify_sparse_map({Point(0,0): '#'}))
    print()
    print_array(gridify_sparse_map({(0,0): '#', (1,1): '#', (-1,1): '_'}))
