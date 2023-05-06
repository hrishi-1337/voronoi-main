from Queue import PriorityQueue
from sympy.geometry import *
from math import sqrt
import matplotlib.pyplot as plt
from util import *
from display import *

class Voronoi:
    def __init__(self, points, bound):
        self.queue = PriorityQueue()
        self.points = points
        self.beach_line = None  
        self.output = []
        self.bound = bound
        for point in points:
            event = Event(point.x, point, None, True)
            self.queue.put((event.x, event))
 
    # Check if the point intersects the beachline arc  
    def check_intersection(self, p, arc):
        if arc is None or arc.point.x == p.x:
            return False, None
        if arc.prev is not None:
            a = (self.parabola_intersection(arc.prev.point, arc.point, p.x)).y
        else:
            a = 0.0
        if arc.next is not None:
            b = (self.parabola_intersection(arc.point, arc.next.point, p.x)).y
        else:
            b = 0.0
        if (arc.prev is None or a <= p.y) and (arc.next is None or p.y <= b):
            px = (arc.point.x ** 2 + (arc.point.y - p.y) ** 2 - p.x ** 2) / (2 * arc.point.x - 2 * p.x)
            # print(px)
            # print(p.y)
            return True, Point(px, p.y)
        return False, None
 
    # Calculate intersection of parabolas
    def parabola_intersection(self, p1, p2, d):
        if p1.x == p2.x:
            y_coor = (p1.y + p2.y) / 2.0
        elif p2.x == d:
            y_coor = p2.y
        elif p1.x == d:
            y_coor = p1.y
            p1 = p2
        else:
            z0 = (p1.x - d) * 2.0 
            z1 = (p2.x - d) * 2.0 
            a = 1.0 / z0 - 1.0 / z1
            b = (p1.y / z0 - p2.y / z1) * -2.0
            c = (p1.y ** 2 + p1.x ** 2 - d ** 2) / z0 - (p2.y ** 2 + p2.x ** 2 - d ** 2) / z1
            y_coor = (-b - sqrt(b ** 2 - 4 * a * c)) / (2 * a)
        x_coor = (p1.x ** 2 + (p1.y - y_coor) ** 2 - d ** 2) / (2 * p1.x - 2 * d)
        result = Point(x_coor, y_coor)
        # print(result)
        return result
 
    # Find the rightmost point and center of a circle 
    def get_circle(self, a, b, c):
        if ((b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y)) > 0:
            return False, None, None            
        c0 = (b.x - a.x)*(a.x+b.x) + (b.y - a.y)*(a.y+b.y)
        c1 = (c.x - a.x)*(a.x+c.x) + (c.y - a.y)*(a.y+c.y)
        c2 = 2.0*((b.x - a.x)*(c.y-b.y) - (b.y - a.y)*(c.x-b.x))
        if (c2 == 0):
            return False, None, None         
        ox = ((c.y - a.y)*c0-(b.y - a.y)*c1)/(c2*1.0)
        oy = ((b.x - a.x)*c1-(c.x - a.x)*c0)/(c2*1.0)
        x = ox + sqrt((a.x - ox) ** 2 + (a.y - oy) ** 2)
        o = Point(ox, oy)
        # print(x,o)
        return True, x, o
 
    # Handles site event 
    def handle_site_event(self, point):
        if self.beach_line is None:
            self.beach_line = Arc(point)
        else:
            arc = self.beach_line
            while arc is not None:
                flag, vertex = self.check_intersection(point, arc)
                if flag:
                    flag, temp = self.check_intersection(point, arc.next)
                    if arc.next is not None and not flag:
                        arc.next.prev = Arc(arc.point, arc, arc.next)
                        arc.next = arc.next.prev
                    else:
                        arc.next = Arc(arc.point, arc)
                    arc.next.edge2 = arc.edge2
                    arc.next.prev = Arc(point, arc, arc.next)
                    arc.next = arc.next.prev
                    arc = arc.next
                    edge1 = Edge(vertex)
                    self.output.append(edge1)
                    arc.prev.edge2 = arc.edge1 = edge1
                    edge2 = Edge(vertex)
                    self.output.append(edge2)
                    arc.next.edge1 = arc.edge2 = edge2
                    self.check_circle_event(arc)
                    self.check_circle_event(arc.prev)
                    self.check_circle_event(arc.next)
                    return
                arc = arc.next
            arc = self.beach_line
            while arc.next is not None:
                arc = arc.next
            arc.next = Arc(point, arc)
            start = Point(0, (arc.next.point.y + arc.point.y) / 2.0)
            edge = Edge(start)
            arc.edge2 = arc.next.edge1 = edge
            self.output.append(edge)
            # print(output)
 
    # Handles circle event 
    def handle_circle_event(self, event):
        if event.valid:
            edge = Edge(event.point)
            self.output.append(edge)
            arc = event.arc
            if arc.prev is not None:
                arc.prev.next = arc.next
                arc.prev.edge2 = edge
            if arc.next is not None:
                arc.next.prev = arc.prev
                arc.next.edge1 = edge
            if arc.edge1 is not None:
                arc.edge1.complete(event.point)
            if arc.edge2 is not None:
                arc.edge2.complete(event.point)
            if arc.prev is not None:
                self.check_circle_event(arc.prev)
            if arc.next is not None:
                self.check_circle_event(arc.next)
 
    # Check if points form a circle  
    def check_circle_event(self, arc):
        if arc.event is not None and arc.event.x != 0:
            arc.event.valid = False
        arc.event = None
        if arc.prev is None or arc.next is None:
            return
        flag, x, center = self.get_circle(arc.prev.point, arc.point, arc.next.point)
        if flag and x > 0:
            arc.event = Event(x, center, arc, False)
            self.queue.put((arc.event.x, arc.event))

    # Complete the edges with the bound
    def complete_edges(self):
        while self.beach_line.next is not None:
            if self.beach_line.edge2 is not None:
                point = self.parabola_intersection(self.beach_line.point, self.beach_line.next.point, self.bound * 4.0)
                self.beach_line.edge2.complete(point)
            self.beach_line = self.beach_line.next

    # Compute voronoi diagram
    def compute(self):
        while not self.queue.empty():
            next_event = self.queue.get()[1]
            if next_event.is_site:
                self.handle_site_event(next_event.point)
            else:
                self.handle_circle_event(next_event)
        self.complete_edges()
        edges = []
        for edge in self.output:
            p1 = edge.start
            p2 = edge.end
            edges.append((p1.x, p1.y, p2.x, p2.y))    
        display_fortune(self.points, edges, self.bound)

if __name__=="__main__":
    bound = 10
    points = [Point(1, 1), Point(2, 3), Point(5, 4), Point(3, 5), Point(4, 2)]
    v = Voronoi(points, bound)
    v.compute()
    