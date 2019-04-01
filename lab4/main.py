import numpy as np
import math
                    #   tha0     ra0     tha1    ra1    thb0     rb0     thb1    rb1     thc0    rc0    thc1   rc1
statistic = np.array([[16.551, 14.899, 30.746, 27.320, 32.822, 29.553, 21.002, 18.793, 17.084, 15.365, 4.544, 3.118],
                      [16.810, 14.292, 22.558, 20.155, 25.314, 22.567, 40.022, 35.436, 29.096, 25.876, 17.519, 16.162],
                      [14.434, 13.046, 28.001, 24.916, 36.918, 32.720, 35.118, 31.145, 38.639, 34.226, 38.841, 34.819],
                      [20.891, 18.696, 32.958, 29.255, 46.677, 41.259, 20.283, 18.164, 23.690, 21.145, 37.324, 33.492],
                      [13.773, 12.468, 28.277, 25.159, 16.909, 15.212, 41.746, 36.944, 29.087, 25.868, 16.717, 15.461],
                      [14.739, 13.313, 36.763, 32.398, 21.889, 19.569, 40.458, 35.817, 21.993, 20.494, 40.099, 35.920],
                      [24.713, 22.040, 34.650, 30.735, 34.998, 31.040, 19.478, 17.460, 30.082, 26.738, 42.244, 37.797],
                      [10.127, 9.278, 33.590, 29.808, 23.285, 20.791, 22.974, 21.353, 18.776, 17.263, 22.099, 20.170],
                      [14.689, 13.269, 12.239, 11.126, 21.561, 19.282, 25.348, 23.430, 34.808, 31.290, 40.895, 36.617],
                      [13.047, 11.833, 35.848, 31.784, 37.778, 33.472, 25.336, 22.586, 26.192, 23.751, 17.519, 16.162],
                      [16.487, 14.843, 38.451, 34.061, 29.376, 26.120, 23.743, 22.025, 18.230, 16.784, 38.841, 34.819],
                      [14.345, 12.968, 18.573, 16.668, 32.822, 29.553, 29.751, 27.282, 37.085, 33.283, 37.324, 33.492]])



if __name__ == "__main__":
    th = statistic[:8, ::2].reshape(-1)
    r = statistic[:8, 1::2].reshape(-1)
    logth = np.array(list(map(math.log, th)))
    logr = np.array(list(map(math.log, r)))
    beta = np.std(logth)/np.std(logr)
    alpha = math.exp(np.average(logth) - beta * np.average(logr))

    print(beta, alpha)

    testth = statistic[8:, ::2].reshape(-1)
    testr = statistic[8:, 1::2].reshape(-1)

    results = list(map(lambda v: (v[0] - alpha * v[1] ** beta), zip(testth, testr)))
    print(results)
    print(th)
