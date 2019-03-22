from Structs import *
import random
import matplotlib.pyplot as plt


def show_plot(triangles=None, points=None, vecs=None, circles=None):
    xrange = (2, 10)
    yrange = (2, 10)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    if triangles:
        for t in triangles:
            patch = t.get_patch()
            ax.add_patch(patch)

    if points:
        for p in points:
            ax.scatter(p.x, p.y)

    if not vecs is None:
        for line in vecs:
            ax.add_line(line.get_line())

    if not circles is None:
        for c in circles:
            circle = plt.Circle((c[0].x, c[0].y), c[1], color='r', fill=False)
            ax.add_artist(circle)
    t = 1
    ax.set_xlim(xrange[0] - t, xrange[1] + t)
    ax.set_ylim(yrange[0] - t, yrange[1] + t)
    plt.show()


def generate_new(edges: List[Edge], point: Point):
    triangles = []
    edges_d = {}

    for edge in edges:
        edge.unvisit()

        if not edge.a.id in edges_d:
            e = Edge(point, edge.a)
            edges_d[edge.a.id] = e
        if not edge.b.id in edges_d:
            e = Edge(point, edge.b)
            edges_d[edge.b.id] = e

        triangle = Triangle()
        triangles.append(triangle)
        triangle.add_edges(edge, edges_d[edge.a.id], edges_d[edge.b.id])

    return triangles


def find(point, triangle: Triangle):
    while True:
        edges = triangle.edges
        center = triangle.point_inside()
        line = Vec(center, point)
        ind = -1
        for i, e in enumerate(edges):
            if line.intersect(Vec(e.a, e.b)):
                ind = i
                break

        if ind == -1:
            return triangle

        triangle = edges[ind].get_another_triangle(triangle.id)


def main_loop(triangles: Dict[str, Triangle], points: List[Point]):
    for i in range(len(points)):
        triangle = list(triangles.values())[random.randint(0, len(triangles) - 1)]
        p = points[i]
        triangle = find(p, triangle)

        edges_d = {}
        next_triangles = [triangle]

        # next_triangle = next_triangles.pop()
        # triangles.pop(next_triangle.id)
        # for j in range(len(next_triangle.edges)):
        #     edge = next_triangle.edges[j]
        #     edge.delete_triangle(next_triangle.id)
        #     if edge.edged:
        #         edges_d[edge.id] = edge
        #     elif len(edge.triangles) == 0:
        #         edges_d.pop(edge.id)
        #     elif len(edge.triangles) == 1:
        #         next_to_add = list(edge.triangles.values())[0]
        #         edges_d[edge.id] = edge
        #         if not next_to_add.visited:
        #             next_to_add.visited = True
        #             next_triangles.append(next_to_add)

        while len(next_triangles) != 0:
            next_triangle = next_triangles.pop()
            condition = next_triangle.delauney(p)
            if not condition:
                triangles.pop(next_triangle.id)
                for j in range(len(next_triangle.edges)):
                    edge = next_triangle.edges[j]
                    edge.delete_triangle(next_triangle.id)
                    if edge.edged:
                        edges_d[edge.id] = edge
                    elif len(edge.triangles) == 0:
                        edges_d.pop(edge.id)
                    elif len(edge.triangles) == 1:
                        edges_d[edge.id] = edge
                        next_to_add = list(edge.triangles.values())[0]
                        if not next_to_add.visited:
                            next_to_add.visited = True
                            next_triangles.append(next_to_add)

        new_t = generate_new(list(edges_d.values()), p)
        for t in new_t:
            triangles[t.id] = t

    return triangles


def generate(xrange, yrange, n):
    points = []
    for i in range(n):
        points.append(Point(random.uniform(*xrange),
                            random.uniform(*yrange)))
    return points


def generate_points(xrange, yrange, n, divisions):
    lenx = xrange[1] - xrange[0]
    leny = yrange[1] - yrange[0]
    points = []
    sx = lenx // divisions
    sy = leny // divisions
    for i in range(divisions):
        for j in range(divisions):
            points += generate((xrange[0] + sx * i, xrange[0] + sx * (i + 1)),
                               (yrange[0] + sy * j, yrange[0] + sy * (j + 1)),
                               n)

    return points


def generate_from_points(points, p):
    points.append(points[0])
    edges = []
    for i in range(len(points) - 1):
        edges.append(Edge(points[i], points[i + 1], edged=True))

    return generate_new(edges, p)


def init(xrange, yrange):
    points = generate_points(xrange, yrange, 2, 8)
    ind = 0
    p = points[ind]

    t = 0.2
    n = 3
    lenx = xrange[1] - xrange[0]
    leny = yrange[1] - yrange[0]
    p_s = [Point(xrange[0] - t, yrange[0] - t, edged=True)]

    for i in range(n):
        p_s.append(Point(xrange[0] + lenx / (n + 1) * (i + 1), yrange[0] - t))

    p_s.append(Point(xrange[1] + t, yrange[0] - t, edged=True))

    for i in range(n):
        p_s.append(Point(xrange[1] + t, yrange[0] + leny / (n + 1) * (i + 1)))

    p_s.append(Point(xrange[1] + t, yrange[1] + t, edged=True))

    for i in range(n):
        p_s.append(Point(xrange[1] - lenx / (n + 1) * (i + 1), yrange[1] + t))

    p_s.append(Point(xrange[0] - t, yrange[1] + t, edged=True))

    for i in range(n):
        p_s.append(Point(xrange[0] - t, yrange[1] - leny / (n + 1) * (i + 1)))

    return generate_from_points(p_s, p), points[ind + 1:]


def main():
    xrange = (2, 10)
    yrange = (2, 10)

    triangles, points = init(xrange, yrange)

    t_d = {}
    for t in triangles:
        t_d[t.id] = t

    triangles = list(main_loop(t_d, points).values())
    circles = []

    for t in triangles:
        cent = t.cent()
        p1 = t.get_vertices()[0]
        circles.append([cent, Vec(cent, p1).length()])

    show_plot(triangles=triangles)


if __name__ == "__main__":
    main()
