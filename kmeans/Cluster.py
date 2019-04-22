import uuid
import numpy as np
import operator

class Point:
    def __init__(self, vector):
        # print(vector)
        self.id = uuid.uuid4()
        self.class_label = vector[-1]
        self.vector = vector[:-1]
        self.cluster_nmb = -1

    def dist(self, other):
        return np.linalg.norm(self.vector - other.vector)
        # vec = self.vector - other.vector
        # return np.sqrt(vec.dot(vec))

    def __hash__(self):
        return self.id.int

    def __repr__(self):
        return str(self.vector)


class Cluster:
    def __init__(self, point: Point):
        self.id = uuid.uuid4()
        self.center = point

    def recalculate_center(self, points):
        lst = list(map(operator.attrgetter('vector'), points))
        res_vec = np.zeros(lst[0].shape[0])
        for p in lst:
            res_vec += p
        self.center = Point(np.concatenate((res_vec / len(points), np.array([0]))))

    def dist(self, point: Point):
        return self.center.dist(point)
