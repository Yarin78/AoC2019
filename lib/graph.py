from queue import Queue
import heapq
import functools
from lib.geo2d import Point, DIRECTIONS, DIRECTIONS_INCL_DIAGONALS


def bfs(graph, start, func=None):
    '''Performs a BFS search in a graph and returns the distans to all nodes visited.
    If func is set, calls func(node, dist) when each node is visited.
    graph: {node: [neighbors]}
    '''
    dist = {}  # node -> distance
    q = Queue()
    q.put(start)
    dist[start] = 0
    while not q.empty():
        current = q.get()
        steps = dist[current]
        if func:
            func(current, steps)
        for neighbor in graph.get(current, []):
            if neighbor not in dist:
                dist[neighbor] = steps + 1
                q.put(neighbor)
    return dist

def dfs(graph, start, func=None):
    '''Performs a DFS search in a graph and returns a set of all nodes visited
    If func is set, calls func(node) when each node is visited.
    graph: {node: [neighbors]}
    '''
    seen = set()
    def go(current):
        nonlocal seen, graph, func
        if current not in seen:
            if func:
                func(current)
            seen.add(current)
            for neighbor in graph.get(current, []):
                go(neighbor)
    go(start)
    return seen

def search_all(graph, graph_search_func, func=None):
    '''Calls the graph_search_func on an arbitrary node, repeats on a non-visited node,
    repeats until all nodes in graph covered.
    Returns an array of the output from the graph_search_func.
    If func is set, calls func(iteration, node) when each node is visited.
    graph: {node: [neighbors]}
    '''
    result = []
    visited = set()
    iteration = 0
    for node in graph.keys():
        if node not in visited:
            res = graph_search_func(graph, node, functools.partial(func, iteration) if func else None)
            result.append(res)
            visited = visited.union(res.keys() if isinstance(res, dict) else res)
            iteration += 1
    return result

def dfs_all(graph, func=None):
    return search_all(graph, dfs, func)

def bfs_all(graph, func=None):
    return search_all(graph, bfs, func)

def _add_reverse_edges(new_graph, graph):
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            if isinstance(neighbor, tuple):
                if neighbor[0] not in new_graph:
                    new_graph[neighbor[0]] = []
                new_graph[neighbor[0]].append([node] + list(neighbor[1:]))
            else:
                if neighbor not in new_graph:
                    new_graph[neighbor] = []
                new_graph[neighbor].append(node)

def reverse_graph(graph):
    '''Creates a new graph that is the edge-reverse of the given graph.
    Works both with or without distances.'''

    new_graph = {}
    _add_reverse_edges(new_graph, graph)
    return new_graph

def symmetric_graph(graph):
    '''Adds reverse edges (in-place) to the graph so it becomes symmetric.
    Works both with or without distances.'''

    new_graph = {node: list(neighbors) for node, neighbors in graph.items()}
    _add_reverse_edges(new_graph, graph)
    return new_graph

def dijkstra(graph, start, func=None):
    '''Performs a shortest-path in a graph and returns the distance to all nodes visited.
    If func is set, calls func(node, dist) when each node is visited.
    graph: {node: [(neighbor, distance)]}
    '''
    dist = {}
    q = []

    def add(node, d):
        nonlocal dist, q
        if node not in dist or d < dist[node]:
            dist[node] = d
            heapq.heappush(q, (d, node))

    add(start, 0)
    while len(q):
        (cur_dist, cur) = heapq.heappop(q)
        if cur_dist == dist[cur]:
            if func:
                func(cur, cur_dist)
            if cur in graph:
                for (x, d) in graph[cur]:
                    add(x, cur_dist + d)

    return dist

def topological_sort(graph):
    '''Performs a topological sort on a graph. Each node in the graph contains
    the dependencies that will be included before the node in the output.
    graph: {node: [neighbors]}
    '''

    q = []  # nodes that can be processed; min-heap so they get in lowest-order
    degree = {}  # node -> outdegree
    reverse = reverse_graph(graph)

    seen = set()
    for node, neighbors in graph.items():
        degree[node] = len(neighbors)
        seen.add(node)
        if degree[node] == 0:
            heapq.heappush(q, node)
        for x in neighbors:
            seen.add(x)

    # In case some nodes (with no dependencies) where left out in the input graph
    for node in seen:
        if node not in degree:
            degree[node] = 0
            heapq.heappush(q, node)

    result = []
    while len(result) < len(seen):
        if not len(q):
            raise Exception('Circular graph')
        current = heapq.heappop(q)
        result.append(current)
        if current in reverse:
            for x in reverse[current]:
                degree[x] -= 1
                assert degree[x] >= 0
                if degree[x] == 0:
                    heapq.heappush(q, x)

    return result


def grid_graph(grid, is_node, get_edge=None, uni_distance=True, num_directions=4):
    '''Converts a grid (line of strings) into a graph given two functions.
    The is_node function takes a Point and character and returns True if
    the position is a node.
    The get_edge function takes Point, char, Point, char (from - to) and
    returns True (or distance) between the nodes. If uni_distance is true,
    no distances will be added, only the edge.
    num_directions should either be 4 (not diagonals) or 8 (with diagonals).'''

    if num_directions == 4:
        directions = DIRECTIONS
    else:
        assert num_directions == 8
        directions = DIRECTIONS_INCL_DIAGONALS

    graph = {}
    ysize = len(grid)
    xsize = len(grid[0])

    for y in range(ysize):
        for x in range(xsize):
            p = Point(x, y)
            c = grid[y][x]
            if is_node(p, c):
                neighbors = []
                for d in directions:
                    np = p + d
                    if np.x >= 0 and np.x < xsize and np.y >= 0 and np.y < ysize:
                        nc = grid[np.y][np.x]
                        if is_node(np, nc):
                            e = get_edge(p, c, np, nc)
                            if e is not None:
                                if uni_distance:
                                    neighbors.append(np)
                                else:
                                    neighbors.append((np, e))
                graph[p] = neighbors

    return graph


if __name__ == "__main__":
    g = {
        0: [(1, 3), (2, 8)],
        1: [(2, 4), (3, 6)],
        2: [(4, 7)],
        3: [(5, 5)],
        4: [(1, 5), (3, 2), (5, 8)],
        6: [(7, 3)]
    }

    h = {
        0: [1, 2, 8],
        1: [2, 3],
        2: [4],
        3: [5],
        4: [1, 3, 5],
        6: [7]
    }

    #h = symmetric_graph(h)
    #a = dfs_all(h)


    #h = symmetric_graph(h)
    #print(bfs_all(h, lambda i, x, steps: print(i,x,steps)))

    topg = {
        0: [5],
        1: [5,2,2],
        2: [5],
        3: [5],
        4: [],
        5: [4],
    }

    #print(topological_sort(topg))

    grid = [
        '......#...',
        '..##..###.',
        '...#...#..',
        '#...#.....'
    ]

    g = grid_graph(grid, is_node=lambda p, c: c == '#', get_edge=lambda p1, c1, p2, c2: 1, uni_distance=False)
    for n, neighbors in g.items():
        print(n, neighbors)
