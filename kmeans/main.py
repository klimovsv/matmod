from Cluster import *
import numpy as np
import operator
import matplotlib.pyplot as plt
import itertools

lables = ["Sex", "Length", "Diameter", "Height", "Whole wheight", "Shucked weight",
          "Viscera weight", "Shell weight", "Rings"]

fig, ax = plt.subplots(nrows=8, ncols=8, figsize=(30, 30))

def compare(old_centers, new_centers):
    lst = list(zip(old_centers, new_centers))
    return all(map(lambda c: np.allclose(c[0].vector - c[1].vector, np.zeros(c[0].vector.shape[0])), lst))


def kmeans(dataset, x_idx, y_idx):
    n = 200
    colors = ['green', 'red', 'blue']
    k_clusters = len(colors)

    points = list(map(lambda x: Point(x), dataset[:n, [x_idx, y_idx]]))
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

        if stationary_count == 2:
            break

    plot = ax[x_idx-1][y_idx-1]
    plot.tick_params(
        which='both',
        bottom='off',
        left='off',
        right='off',
        top='off'
    )
    for p in points:
        vec = p.vector
        plot.scatter(vec[0], vec[1], color=colors[p.cluster_nmb])

    plot.set_xlabel(lables[x_idx])
    plot.set_ylabel(lables[y_idx])


def main():
    data = np.genfromtxt('abalone.data', delimiter=',')
    np.random.shuffle(data)
    pairs = list(itertools.product(range(1, len(lables)), range(1, len(lables))))
    for x, y in pairs:
        kmeans(data, x, y)
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    plt.savefig("res.png")


if __name__ == '__main__':
    main()
