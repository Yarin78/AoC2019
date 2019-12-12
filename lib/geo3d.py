EPSILON = 1e-9

def almost_equal(a, b):
    return abs(a-b) < EPSILON

class Point:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point(self.x + other.x, self.y+other.y, self.z+other.z)

    def __abs__(self):
        return Point(abs(self.x), abs(self.y), abs(self.z))

    def __eq__(self, other):
        return other and almost_equal(self.x, other.x) and almost_equal(self.y, other.y) and almost_equal(self.z, other.z)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if almost_equal(self.z, other.z):
            if almost_equal(self.y, other.y):
                if almost_equal(self.x, other.x):
                    return 0
                return self.x < other.x
            return self.y < other.y
        return self.z < other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __str__(self):
        return '({0}, {1}, {2})'.format(self.x, self.y, self.z)

    def __repr__(self):
        return self.__str__()
