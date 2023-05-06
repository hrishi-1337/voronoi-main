import math

class Halfplane:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    
    def __repr__(self):
        return "Halfplane({}, {}, {})".format(self.a, self.b, self.c)
    
    def __lt__(self, other):
        return self.angle() < other.angle()
    
    def angle(self):
        return math.atan2(-self.a, self.b)

    def intersect(self, h1, h2):
        det = h1.a * h2.b - h2.a * h1.b
        if det == 0:
            return False
        x = (h2.c * h1.b - h1.c * h2.b) / det
        y = (h1.c * h2.a - h2.c * h1.a) / det
        return h1.contains(x, y) and h2.contains(x, y)

    def intersect_point(self, other):
        det = self.a * other.b - other.a * self.b
        if det == 0:
            return None  
        x = (other.c * self.b - self.c * other.b) / det
        y = (self.c * other.a - other.c * self.a) / det
        return x, y

    def contains(self, x, y):
        return self.a * x + self.b * y + self.c <= 0
    
class Site:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.edges = []

    def __repr__(self):
        return "Site({}, {}, {})".format(self.x, self.y, self.edges)

class Event:
    def __init__(self, x, point, arc, is_site):
        self.is_site = is_site
        self.x = x
        self.point = point
        self.arc = arc
        self.valid = True

class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.incident_edge = None

    def __repr__(self):
        return "Vertex({}, {}, {})".format(self.x, self.y, self.incident_edge)

class HalfEdge:
    def __init__(self, origin, twin, face, is_twin):
        self.origin = origin
        self.twin = twin
        self.face = face
        self.is_twin = is_twin
        self.origin_edge = None

class Arc:
    def __init__(self, point, prev_arc=None, next_arc=None):
        self.point = point
        self.prev = prev_arc
        self.next = next_arc
        self.event = None
        self.edge1 = None
        self.edge2 = None

class Edge:
    def __init__(self, point):
        self.start = point
        self.end = None
        self.done = False

    def complete(self, point):
        if not self.done:
            self.end = point
            self.done = True

class Face:
    def __init__(self, site):
        self.site = site
        self.edges = []

    def contains(self, vertex):
        for edge in self.edges:
            if edge.origin == vertex:
                return True
        return False

class DCEL:
    def __init__(self, vertex_list = [], edge_list = [], site=None, bound=[]):
        self.vertex_list = vertex_list
        self.edge_list = edge_list
        self.vertices = []
        self.edges = []
        self.faces = []
        self.site = site
        self.bound = bound
        if vertex_list != []:
            self.build_dcel()

    def build_dcel(self):
        edge_dict = {}

        for vertex in self.vertex_list:
            vertex = Vertex(vertex.x, vertex.y)
            self.vertices.append(vertex)

        for edge_start, edge_end in self.edge_list:
            half_edge1 = HalfEdge(edge_start)
            half_edge2 = HalfEdge()
            edge = Edge(half_edge1, half_edge2)
            self.edges.append(edge)
            edge_dict[edge] = (half_edge1, half_edge2)

            half_edge1.edge = edge
            half_edge2.edge = edge
            half_edge1.vertex = self.vertices[edge_start]
            half_edge2.vertex = self.vertices[edge_end]

        for edge, (half_edge1, half_edge2) in edge_dict.items():
            half_edge1.next = half_edge2
            half_edge2.prev = half_edge1

        outer_face = Face()
        self.faces.append(outer_face)

        bounding_half_edges = []
        for i in range(len(self.bound)):
            start_vertex = self.vertices[self.bound[i]]
            end_vertex = self.vertices[self.bound[(i+1)%len(self.bound)]]
            half_edge = HalfEdge()
            half_edge.vertex = end_vertex
            bounding_half_edges.append(half_edge)

        for i in range(len(bounding_half_edges)):
            bounding_half_edges[i].next = bounding_half_edges[(i+1)%len(bounding_half_edges)]
            bounding_half_edges[(i+1)%len(bounding_half_edges)].prev = bounding_half_edges[i]

        for half_edge in bounding_half_edges:
            half_edge.face = outer_face
            outer_face.half_edge = half_edge
