from Cluster import *
import numpy as np
import operator
import matplotlib.pyplot as plt
import itertools
import pandas

lables = ["Sex", "Length", "Diameter", "Height", "Whole wheight", "Shucked weight",
          "Viscera weight", "Shell weight", "Rings"]

fig, ax = plt.subplots(nrows=8, ncols=8, figsize=(30, 30))


def compare(old_centers, new_centers):
    lst = list(zip(old_centers, new_centers))
    return all(map(lambda c: np.allclose(c[0].vector - c[1].vector, np.zeros(c[0].vector.shape[0])), lst))


def predict(clusters, point):
    best = min(enumerate(clusters), key=lambda v: v[1].dist(point))
    return best[0]


def kmeans(dataset, idx, class_coord):
    points = list(map(lambda x: Point(x), dataset[:, idx + [class_coord]]))

    colors = ['red', 'blue']
    labels_set = set(map(operator.attrgetter('class_label'), points))
    k_clusters = len(colors)

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

    if len(idx) == 2:
        x_idx = idx[0]
        y_idx = idx[1]
        plot = ax[x_idx - 1][y_idx - 1]
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

    return clusters, cluster_points


def main():
    # data = np.loadtxt('abalone.data', delimiter=',')
    data = pandas.read_csv('abalone.data', sep=",", header=None)

    def ret(x):
        if x == "M":
            return 1
        elif x == "F":
            return 1
        elif x == "I":
            return 2

    first_col = np.array(list(map(lambda x: ret(x[0]), data.values)))
    data = data.values
    data[:, [0]] = first_col.reshape((len(data), 1))
    data = np.array(data.tolist(), dtype=np.float)
    np.random.shuffle(data)

    two_features = True
    if two_features:
        n = 100
        pairs = list(itertools.product(range(1, len(lables)), range(1, len(lables))))
        for x, y in pairs:
            kmeans(data[:n], [x, y], 0)
        plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
        plt.savefig("res.png")
    else:
        ind = [1, 3, 5, 7]
        clusters, cluster_points = kmeans(data, ind, -1)
        for i, points in cluster_points.items():
            labels = list(map(operator.attrgetter('class_label'), points))
            avg = sum(labels) / len(points)
            print(avg, max(labels), min(labels), np.std(labels), i)

        point = Point(data[500, ind + [-1]])
        print(point.class_label)
        best = predict(clusters, point)
        print(best)


if __name__ == '__main__':
    main()
