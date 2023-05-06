from heapq import heappop, heappush
from scipy.spatial import HalfspaceIntersection
import numpy as np
from sympy.geometry import *
from util import *
from display import *

# Find perpendicalar bisector
def bisector(p1, p2):
    mid = Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    slope = -dx / dy
    intercept = mid.y - (slope * mid.x)
    if p1.y < slope * p1.x + intercept:         
        a, b, c = -slope, 1, -intercept
    else:        
        a, b, c = slope, -1, intercept     
    return Halfplane(a, b, c)

# Sort-and-incremental algorithm for halfplane intersection
def sort_and_incremental_intersect(halfplanes, bound):
    left_hp = Halfplane(-1, 0, 0)
    bottom_hp = Halfplane(0, -1, 0)
    right_hp = Halfplane(1, 0, -bound)
    top_hp = Halfplane(0, 1, -bound)
    halfplanes.extend([left_hp, bottom_hp, right_hp, top_hp])
    halfplanes.sort(key=lambda h: -h.angle())
    heap = [halfplanes[0]]
    for i in range(1, len(halfplanes)):
        h = halfplanes[i]
        while len(heap) > 1 and not heap[0].intersect(heap[1], h):
            heappop(heap)
        heappush(heap, h)
    while len(heap) > 1 and not heap[0].intersect(heap[1], heap[-1]):
        heappop(heap)
    vertices = []
    for i in range(len(heap)):
        p = heap[i].intersect_point(heap[(i+1)%len(heap)])
        if p != None:
            if p[0]  < 0 or p[1] < 0:
                continue
            else:
                vertices.append(p)
    return vertices

# Scipy halfplane intersection
def scipy_intersect(center, halfplanes, bound):
    coeffs = np.array([(hp.a, hp.b, hp.c) for hp in halfplanes])
    bbox = np.array([[-1, 0, 0],
                       [0, -1, 0],
                       [1, 0, -bound],
                       [0, 1, -bound]])
    feasible_point = np.array([float(center.x), float(center.y)])
    hs = HalfspaceIntersection(np.vstack([coeffs, bbox]), feasible_point)
    vertices = hs.intersections
    vertices_rounded = np.round(vertices, decimals=2)
    return(vertices_rounded)


# Main function
def voronoi(points, bound):
    n = len(points)
    cells = []
    for i in range(n):
        halfplanes = []
        center = points[i]
        for j in range(n):
            if i == j:
                continue  
            bis = bisector(points[i], points[j])
            if bis is not None:
                halfplanes.append(bis)        
        # cell = sort_and_incremental_intersect(halfplanes)
        cell = scipy_intersect(center, halfplanes, bound)
        cells.append((center, cell))
    display_naive(cells, n)

# if __name__=="__main__":
#     points = [Point(1, 1), Point(2, 3), Point(4, 2), Point(5, 4), Point(3, 5)]
#     voronoi(points, 10)