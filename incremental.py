import numpy as np
from sympy.geometry import *
from util import *

def voronoi(points, bound):
    n = len(points)
    active_points = []
    p = points.pop()
    active_points.append(p)
    p1 = Point(0,0)
    p2 = Point(0,bound)
    p3 = Point(bound,0)
    p4 = Point(bound,bound)
    vertex_list = [p1, p2, p3, p4]
    edge_list = [(p1, p2), (p2, p3), (p3, p4), (p4, p1)]
    G = DCEL(vertex_list, edge_list, p, bound)
    for i in range(n-1):
       pass


points = [Point(1, 1), Point(2, 3), Point(4, 2), Point(5, 4), Point(3, 5)]
voronoi(points, 10)