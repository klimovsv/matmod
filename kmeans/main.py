from Cluster import *
import numpy as np
import operator
import matplotlib.pyplot as plt

def compare(old_centers, new_centers):
    lst = list(zip(old_centers, new_centers))
    return all(map(lambda c: np.allclose(c[0].vector - c[1].vector, np.zeros(c[0].vector.shape[0])), lst))


def main():
    colors = ['green', 'red', 'blue']
    k_clusters = len(colors)

    data = np.genfromtxt('abalone.data', delimiter=',')

    points = list(map(lambda x: Point(x), data[:100, 4:6]))
    np.random.shuffle(points)
    kpoints = points[:k_clusters]
    clusters = list(map(lambda x: Cluster(x), kpoints))
    stationary_count = 0
    while True:
        for point in points:
            min_dist = min(enumerate(clusters), key=lambda cluster: cluster[1].dist(point))
            point.cluster_nmb = min_dist[0]

        cluster_points = {}
        for point in points:
            if not cluster_points.get(point.cluster_nmb):
                cluster_points[point.cluster_nmb] = []

            cluster_points[point.cluster_nmb].append(point)

        old_centers = list(map(operator.attrgetter('center'), clusters))
        for k, v in cluster_points.items():
            clusters[k].recalculate_center(v)
        new_centers = list(map(operator.attrgetter('center'), clusters))

        if compare(old_centers, new_centers):
            stationary_count += 1
        else:
            stationary_count = 0

        if stationary_count == 3:
            break

    for p in points:
        vec = p.vector
        plt.scatter(vec[0], vec[1], color=colors[p.cluster_nmb])

    plt.show()



if __name__ == '__main__':
    main()
