import uuid
import math
from typing import *
import numpy as np
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib.lines import Line2D

Point = None
Triangle = None


class Vec:
    def __init__(self, a: Point, b: Point):
        self.a = a
        self.b = b
        self.x = b.x - a.x
        self.y = b.y - a.y

    def length(self):
        return math.sqrt(self.x**2+self.y**2)
    def get_line(self):
        return Line2D([self.a.x, self.b.x], [self.a.y, self.b.y])

    def cross(self, other):
        return np.cross([self.x, self.y], [other.x, other.y])


    def intersect(self, other):
        start1 = self.a
        start2 = other.a
        end1 = self.b
        end2 = other.b
        dir1 = Point(self.x, self.y)
        dir2 = Point(other.x, other.y)
        a1 = -dir1.y
        b1 = +dir1.x
        d1 = -(a1 * start1.x + b1 * start1.y)
        a2 = -dir2.y
        b2 = +dir2.x
        d2 = -(a2 * start2.x + b2 * start2.y)


        seg1_line2_start = a2 * start1.x + b2 * start1.y + d2
        seg1_line2_end = a2 * end1.x + b2 * end1.y + d2
        seg2_line1_start = a1 * start2.x + b1 * start2.y + d1
        seg2_line1_end = a1 * end2.x + b1 * end2.y + d1

        if seg1_line2_start * seg1_line2_end >= 0 or seg2_line1_start * seg2_line1_end >= 0:
            return False
        else:
            return True

    @staticmethod
    def inside_triangle(vec1, vec2, p):
        diag = Vec(Point(0, 0), Point(vec1.x + vec2.x, vec1.y + vec2.y))
        x = p.x + diag.x / 4
        y = p.y + diag.y / 4
        return Point(x, y)


class Edge:
    def __init__(self, a: Point, b: Point, edged=False):
        self.id = uuid.uuid4().int
        self.a = a
        self.b = b
        self.edged = edged
        self.triangles = {}

    def get_another_triangle(self, t_id):
        for id, t in self.triangles.items():
            if id != t_id:
                return t

    def add_triangle(self, triangle: Triangle):
        self.triangles[triangle.id] = triangle

    def delete_triangle(self, t_id: uuid.UUID):
        self.triangles.pop(t_id)

    def unvisit(self):
        for t in self.triangles.values():
            t.visited = False


class Point:
    def __init__(self, x, y, edged=False):
        self.id = uuid.uuid4().int
        self.x = x
        self.y = y
        self.edged = edged

    def __str__(self):
        return "({} , {})".format(self.x, self.y)


class Triangle:
    def __init__(self):
        self.id = uuid.uuid4().int
        self.edges = []
        self.color = "#0000ff"
        self.p = None
        self.visited = False
        self.cent_prop = None

    def get_vertices(self):
        if self.p is None:
            p = {}
            for e in self.edges:
                if e.a.id not in p:
                    p[e.a.id] = e.a
                if e.b.id not in p:
                    p[e.b.id] = e.b
            self.p = list(p.values())

        return self.p

    def add_edge(self, edge: Edge):
        self.edges.append(edge)
        edge.add_triangle(self)

    def add_edges(self, *args):
        for e in args:
            self.edges.append(e)
            e.add_triangle(self)

    def set_color(self, color):
        self.color = color

    def get_patch(self):
        p = self.get_vertices()
        verts = [(p.x, p.y) for p in p] + [(p[0].x, p[0].y)]
        codes = [Path.MOVETO] + [Path.LINETO for i in range(len(p) - 1)] + [Path.CLOSEPOLY]
        return patches.PathPatch(Path(verts, codes), edgecolor=self.color,
                                 facecolor='none', lw=2, linewidth=0.01)

    def inside(self, point: Point):
        area = self.area()
        res = 0
        eps = 10 ** -5
        for edge in self.edges:
            t = Triangle()
            t.add_edges(Edge(point, edge.a), Edge(edge.a, edge.b), Edge(point, edge.b))
            res += t.area()
        return res - area <= 0 and abs(res - area) <= eps

    def cent(self):

        if self.cent_prop is not None:
            return self.cent_prop

        [p1, p2, p3] = self.get_vertices()
        ax, ay, bx, by, cx, cy = p1.x, p1.y, p2.x, p2.y, p3.x, p3.y
        dx = bx - ax
        dy = by - ay
        ex = cx - ax
        ey = cy - ay
        bl = dx * dx + dy * dy
        cl = ex * ex + ey * ey
        d = dx * ey - dy * ex
        x = ax + (ey * bl - dy * cl) * 0.5 / d
        y = ay + (dx * cl - ex * bl) * 0.5 / d

        self.cent_prop = Point(x, y)
        return self.cent_prop

    def point_inside(self):
        [p1, p2, p3] = self.get_vertices()
        vec1 = Vec(p1, p2)
        vec2 = Vec(p1, p3)

        return Vec.inside_triangle(vec1, vec2, p1)


    def delauney(self, point: Point):
        x0, y0 = point.x, point.y
        [p1, p2, p3] = self.get_vertices()
        cent = self.cent()
        r = Vec(cent, p1).length()
        condition = (x0 - cent.x)**2 + (y0 - cent.y)**2 >= r**2
        return condition
