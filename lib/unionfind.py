class UnionFind:
    def __init__(self, n):
        '''Initializes a new UnionFind structure with n elements.'''
        self.p = [i for i in range(n)]
        self.size = [1 for i in range(n)]

    def find_set(self, e):
        v = e
        while self.p[v] != v:
            v = self.p[v]
        root = v
        # Path compression
        while self.p[e] != root:
            t = e
            e = self.p[e]
            self.p[t] = root
        return root

    def union_set(self, a, b):
        a = self.find_set(a)
        b = self.find_set(b)
        if a == b:
            return
        if self.size[b] > self.size[a]:
            c = a
            a = b
            b = c
        self.p[b] = a
        self.size[a] += self.size[b]
