# Setups combinatorial tables for efficient modular arithmetic when MOD is a prime
#
# Requires O(N) space and time in setup, so only useful if mod is relatively small

MOD = 0
_fact = None         # _fact[x] = x! modulo MOD
_inverse = None      # x * _inverse[x] = 1 modulo MOD

def calc_inverse(a, m):
    a %= m
    if a == 1:
        return 1
    return (1 - m * calc_inverse(m % a, a)) // a % m


def _choose(n, k):
    if k > n or k < 0:
        return 0

    d = _fact[k] * _fact[n-k]
    d %= MOD
    return (_fact[n] * _inverse[d]) % MOD


def choose(n, k):
    v = 1
    while n > 0:
      v *= _choose(n % MOD, k % MOD)
      v %= MOD
      n //= MOD
      k //= MOD
    return v


def factorial(n):
    '''n! in mod MOD'''
    # TODO: If n >= MOD, use Wilson's theorem, http://en.wikipedia.org/wiki/Wilson%27s_theorem
    return _fact[n]


def init(mod):
    global MOD, _fact, _inverse
    MOD = mod
    _fact = [1] * mod
    for i in range(1, mod):
        _fact[i] = (i * _fact[i-1]) % MOD
    _inverse = [calc_inverse(i, MOD) if i else 0 for i in range(mod)]
