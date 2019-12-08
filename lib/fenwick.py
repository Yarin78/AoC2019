# Datastructure for storing and updating integer values in an array in log(n) time
# and answering queries "what is the sum of all value in the array between 0 and x?" in log(n) time
#
# Also called Binary Indexed Tree (BIT). See http://codeforces.com/blog/entry/619

class FenwickTree:

    def __init__(self, exp):
        '''Creates a FenwickTree with range 0..(2^exp)-1'''
        self.exp = exp
        self.t = [0] * 2 ** (exp+1)

    def query_range(self, x, y):
        '''Gets the sum of the values in the range [x, y)'''
        return self.query(y) - self.query(x)

    def query(self, x, i=-1):
        '''Gets the sum of the values in the range [0, x).'''
        if i < 0:
            i = self.exp
        return (x&1) * self.t[(1<<i)+x-1] + self.query(x//2, i-1) if x else 0

    def insert(self, x, v, i=-1):
        '''Adds the value v to the position x'''
        if i < 0:
            i = self.exp
        self.t[(1<<i)+x] += v
        return self.t[(1<<i)+x] + (self.insert(x//2, v, i-1) if i > 0 else 0)
