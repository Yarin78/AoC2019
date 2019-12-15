import math

EPSILON = 1e-9

def almost_equal(a, b):
    return abs(a-b) < EPSILON

def almost_zero(a):
    return abs(a) < EPSILON

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y+other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y-other.y)

    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)

    def __abs__(self):
        return Point(abs(self.x), abs(self.y))

    def __eq__(self, other):
        return other and almost_equal(self.x, other.x) and almost_equal(self.y, other.y)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if almost_equal(self.y, other.y):
            if almost_equal(self.x, other.x):
                return 0
            return self.x < other.x
        return self.y < other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return '({0}, {1})'.format(self.x, self.y)

    def __repr__(self):
        return self.__str__()

    def rotate(self, theta):
        return Point(math.cos(theta) * self.x - math.sin(theta) * self.y, math.sin(theta) * self.x + math.cos(theta) * self.y)

    def norm_sqr(self):
        return self.x*self.x + self.y*self.y


class Line:

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __hash__(self):
        return hash((self.a, self.b))

    def __str__(self):
        return '{{{0} - {1}}}'.format(self.a, self.b)

    def __repr__(self):
        return self.__str__()

    def segment_length(self):
        return math.sqrt((a-b).norm_sqr())

    def is_parallel_to(self, other):
        return almost_zero(det(self.b - self.a, other.b - other.a))

    def unit_vector(self):
        length = self.segment_length()
        return Point((b.x - a.x) / length, (b.y - a.y) / length)


def det(a, b):
    return a.x*b.y-a.y*b.x

def dot(a, b):
    return a.x*b.x+a.y*b.y

def cross(a, b, c):
    return det(b-a, c-a)

def is_point_on_line(line, p):
    return almost_zero(cross(line.a, line.b, p))

def is_point_on_line_segment(line, p):
    return is_point_on_line(line, p) and dot(line.a - p, p - line.b) >= 0

def point_line_distance(line, p):
    v = line.b - line.a
    u = p - line.a
    d = dot(v, u) / v.norm_sqr()
    return math.sqrt(math.pow(u.x - v.x*d, 2) + math.pow(u.y - v.y*d, 2))

def point_line_segment_distance(line, p):
    v = line.b - line.a
    u = p - line.a
    d = dot(v, u) / v.norm_sqr()
    if d > 0 and d < 1:
        return math.sqrt(math.pow(u.x - v.x*d, 2) + math.pow(u.y - v.y*d, 2))
    return math.sqrt(min((line.a - p).norm_sqr(), (line.b - p).norm_sqr()))

def project_point_onto_line(line, p):
    b = line.b - line.a
    a = p - line.a
    d = dot(b,a) / b.norm_sqr()
    res = Point(line.a.x + b.x * d, line.a.y + b.y * d)
    return res

def vector_transform(p, u, v):
    '''Transforms point p the same way point u has been transformed into point v (from origo)'''
    d0 = u.norm_sqr()
    p = Point(det(u, p), dot(u, p))
    return Point(det(v, p) / d0, dot(v, p) / d0)

def line_intersect(a, b):
    '''Returns the intersection point of two lines, or None if they are parallel'''
    difv = b.a - a.a
    av = a.b - a.a
    bv = b.a - b.b
    d = det(av,bv)
    fa = det(difv, bv)
    fb = det(av, difv)
    if almost_zero(d):
        return None
    if d < 0:
        d = -d
        fa = -fa
        fb = -fb
    return a.a + av * (fa/d)

def line_intersect_segment(a, b):
    '''Returns the intersection point of two line segments, or None if they don't intersect'''
    difv = b.a - a.a
    av = a.b - a.a
    bv = b.a - b.b
    d = det(av,bv)
    fa = det(difv, bv)
    fb = det(av, difv)
    if almost_zero(d):
        return None
    if d < 0:
        d = -d
        fa = -fa
        fb = -fb
    if fa<0 or fa>d or fb<0 or fb>d:
        return False
    return a.a + av * (fa/d)

def merge_line_segments(a, b):
    if not a.is_parallel_to(b):
        return None
    if (not is_point_on_line_segment(a, b.a) and not is_point_on_line_segment(a, b.b) and
        not is_point_on_line_segment(b, a.a) and not is_point_on_line_segment(b, a.b)):
        return None
    points = sorted([a.a, a.b, b.a, b.b])
    return Line(points[0], points[3])

def line_equation(line):
    '''Gets an equation on the form ax+by=c for this line where a^2+b^2 = 1'''
    if (abs(line.a.x-line.b.x) > abs(line.a.y-line.b.y)):
        ea = (line.a.y-line.b.y) / (line.b.x-line.a.x)
        eb = 1
    else:
        ea = 1
        eb = (line.a.x-line.b.x)/(line.b.y-line.a.y)

    d = math.sqrt(ea*ea + eb*eb)
    ea /= d
    eb /= d
    ec = ea * line.a.x + eb * line.a.y
    return [ea, eb, ec]


NORTH = UP = Point(0, -1)
NORTH_EAST = UP_RIGHT = Point(1, -1)
EAST = RIGHT = Point(1, 0)
SOUTH_EAST = DOWN_RIGHT = Point(1,1)
SOUTH = DOWN = Point(0, 1)
SOUTH_WEST = DOWN_LEFT = Point(-1,1)
WEST = LEFT = Point(-1, 0)
NORTH_WEST = UP_LEFT = Point(-1, -1)

DIRECTIONS = [NORTH, EAST, SOUTH, WEST]
DIRECTIONS_INCL_DIAGONALS = [NORTH, NORTH_EAST, EAST, SOUTH_EAST, SOUTH, SOUTH_WEST, WEST, NORTH_WEST]


DIRECTION_MAP = {
    'U': NORTH,
    'D': SOUTH,
    'R': EAST,
    'L': WEST,

    'N': NORTH,
    'S': SOUTH,
    'E': EAST,
    'W': WEST,

    'NW': NORTH_WEST,
    'SW': SOUTH_WEST,
    'NE': NORTH_WEST,
    'SE': SOUTH_EAST
}
