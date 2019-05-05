import numpy as np
import math
from numpy import genfromtxt

table_part3 = genfromtxt('lab3.csv', delimiter=',')[1:, :-1]
table_part2 = genfromtxt('lab2.csv', delimiter=',')[1:]

#   tha0     ra0     tha1    ra1    thb0     rb0     thb1    rb1     thc0    rc0    thc1   rc1
table_part1 = np.array([[16.551, 14.899, 30.746, 27.320, 32.822, 29.553, 21.002, 18.793, 17.084, 15.365, 4.544, 3.118],
                        [16.810, 14.292, 22.558, 20.155, 25.314, 22.567, 40.022, 35.436, 29.096, 25.876, 17.519,
                         16.162],
                        [14.434, 13.046, 28.001, 24.916, 36.918, 32.720, 35.118, 31.145, 38.639, 34.226, 38.841,
                         34.819],
                        [20.891, 18.696, 32.958, 29.255, 46.677, 41.259, 20.283, 18.164, 23.690, 21.145, 37.324,
                         33.492],
                        [13.773, 12.468, 28.277, 25.159, 16.909, 15.212, 41.746, 36.944, 29.087, 25.868, 16.717,
                         15.461],
                        [14.739, 13.313, 36.763, 32.398, 21.889, 19.569, 40.458, 35.817, 21.993, 20.494, 40.099,
                         35.920],
                        [24.713, 22.040, 34.650, 30.735, 34.998, 31.040, 19.478, 17.460, 30.082, 26.738, 42.244,
                         37.797],
                        [10.127, 9.278, 33.590, 29.808, 23.285, 20.791, 22.974, 21.353, 18.776, 17.263, 22.099, 20.170],
                        [14.689, 13.269, 12.239, 11.126, 21.561, 19.282, 25.348, 23.430, 34.808, 31.290, 40.895,
                         36.617],
                        [13.047, 11.833, 35.848, 31.784, 37.778, 33.472, 25.336, 22.586, 26.192, 23.751, 17.519,
                         16.162],
                        [16.487, 14.843, 38.451, 34.061, 29.376, 26.120, 23.743, 22.025, 18.230, 16.784, 38.841,
                         34.819],
                        [14.345, 12.968, 18.573, 16.668, 32.822, 29.553, 29.751, 27.282, 37.085, 33.283, 37.324,
                         33.492]])


def get_alpha(ksi1, ksi2):
    ksi1 = np.array(list(map(lambda x: x * 1000, ksi1)))
    ksi2 = np.array(list(map(lambda x: x * 1000, ksi2)))
    logth = np.log(ksi1)
    logr = np.log(ksi2)
    beta = np.std(logth) / np.std(logr)
    alpha = math.exp(np.mean(logth) - beta * np.mean(logr))
    return alpha, beta


def generateF(array, l, r, n):
    step = (r - l) / n
    n_entries = len(array)
    F = []
    for i in range(1, 1 + n):
        tmp = list(filter(lambda v: v <= l + step * i, array))
        F.append(len(tmp) / n_entries)
    return F


def test(ksi1t, ksi2t, alpha, beta):
    testthapr = np.array(list(map(lambda v: alpha * (v * 1000) ** beta, ksi2t)))
    sortedtest = np.sort(np.array(list(map(lambda x: x * 1000, ksi1t))))
    sortedtestapr = np.sort(testthapr)

    left = min(sortedtestapr[0], sortedtest[0])
    right = max(sortedtestapr[-1], sortedtest[-1])
    steps = 4
    F1 = generateF(sortedtest, left, right, steps)
    F2 = generateF(sortedtestapr, left, right, steps)
    res = max(map(lambda v: abs(v[0] - v[1]), zip(F1, F2)))
    return res


def filtered(arr):
    return np.array(list(filter(lambda x: not np.isnan(x), arr.reshape(-1))))

def print_res(*args):
    print("alpha: {}, beta: {}, criteria: {}, eps: {}".format(*args))

def test_hypot():
    # hypot 1
    th = table_part1[:6, ::2].reshape(-1)
    r = table_part1[:6, 1::2].reshape(-1)
    alpha, beta = get_alpha(th, r)

    testth = table_part1[6:, ::2].reshape(-1)
    testr = table_part1[6:, 1::2].reshape(-1)
    res = test(testth, testr, alpha, beta)
    allowed = np.sqrt(np.abs(0.5 * np.log(beta)))
    print_res(alpha, beta, res, allowed)

    # hypot2
    tha0 = filtered(table_part2[:, 0])
    tha1 = filtered(table_part2[:, 2])
    thb0 = filtered(table_part2[:, 4])
    thb1 = filtered(table_part2[:, 6])
    thc0 = filtered(table_part2[:, 8])
    thc1 = filtered(table_part2[:, 10])
    th = np.concatenate((tha0[::2], tha1[::2], thb0[::2], thb1[::2], thc0[::2], thc1[::2]))
    th_test = np.concatenate((tha0[1::2], tha1[1::2], thb0[1::2], thb1[1::2], thc0[1::2], thc1[1::2]))

    LL = filtered(table_part2[::2, 1::2])
    LL_test = filtered(table_part2[1::2, 1::2])

    alpha3, beta3 = get_alpha(th, LL)
    res = test(th_test, LL_test, alpha, beta)
    allowed = np.sqrt(np.abs(0.5 * np.log(beta3)))
    print_res(alpha3, beta3, res, allowed)

    # hypot 3
    alphas = []
    betas = []
    ksi3 = filtered(table_part3[::3, :8:2])
    ksi4 = filtered(table_part3[::3, 1:9:2])
    ksi5 = filtered(table_part3[1::3, 1:9:2])
    ksi6 = filtered(table_part3[2::3, 1:9:2])
    for i, arr in enumerate([ksi4, ksi5, ksi6]):
        a, b = get_alpha(ksi3, arr)
        alphas.append(a)
        betas.append(b)

    testksi3 = filtered(table_part3[::3, 8::2])
    testksi4 = filtered(table_part3[::3, 9::2])
    testksi5 = filtered(table_part3[1::3, 9::2])
    testksi6 = filtered(table_part3[2::3, 9::2])
    for i, arr in enumerate([testksi4, testksi5, testksi6]):
        res = test(testksi3, arr, alphas[i], betas[i])
        allowed = np.sqrt(np.abs(0.5 * np.log(betas[i])))
        print_res(alphas[i], betas[i], res, allowed)

    ksi2 = 857038
    ksi1 = alpha * ksi2 ** beta
    ksi3 = (ksi1 / alpha3) ** (1 / beta3)
    # print(alphas, betas)
    betas[0] = 1
    alphas[0] = np.mean(filtered(table_part3[::3, :8:2]))/np.mean(filtered(table_part3[::3, 1:9:2]))
    # print(alphas, betas)
    ksi4 = (ksi3 / alphas[0]) ** (1 / betas[0])
    ksi5 = (ksi3 / alphas[1]) ** (1 / betas[1])
    ksi6 = (ksi3 / alphas[2]) ** (1 / betas[2])

    buy_sum = ksi4 + ksi5 + ksi6
    pksi4, pksi5, pksi6 = ksi4 / buy_sum, ksi5 / buy_sum, ksi6 / buy_sum
    # print(pksi4, pksi5, pksi6)
    # print(pksi4 + pksi5 + pksi6)

    S = ksi4 * pksi4 * 24 + ksi5 * pksi5 * 36 + ksi6 * pksi6 * 110
    Smean = S / buy_sum
    res = Smean * ksi2
    print("average: ", Smean)
    print(ksi1)
    print("daily income: ", res)


def main():
    th = table_part1[:, ::2].reshape(-1)
    r = table_part1[:, 1::2].reshape(-1)
    alpha, beta = get_alpha(th, r)
    print(alpha, beta)

    th = filtered(table_part2[:, ::2])
    LL = filtered(table_part2[:, 1::2])
    alpha3, beta3 = get_alpha(th, LL)
    print(alpha3, beta3)

    alphas = []
    betas = []
    ksi3 = filtered(table_part3[::3, ::2])
    ksi4 = filtered(table_part3[::3, 1::2])
    ksi5 = filtered(table_part3[1::3, 1::2])
    ksi6 = filtered(table_part3[2::3, 1::2])
    for i, arr in enumerate([ksi4, ksi5, ksi6]):
        a, b = get_alpha(ksi3, arr)
        alphas.append(a)
        betas.append(b)

    ksi2 = 857038
    ksi1 = alpha * ksi2 ** beta
    ksi3 = (ksi1 / alpha3) ** (1 / beta3)
    ksi4 = (ksi3 / alphas[0]) ** (1 / betas[0])
    ksi5 = (ksi3 / alphas[1]) ** (1 / betas[1])
    ksi6 = (ksi3 / alphas[2]) ** (1 / betas[2])

    buy_sum = ksi4 + ksi5 + ksi6
    S = ksi4 * 0.5 * 24 + ksi5 * 0.25 * 36 + ksi6 * 0.25 * 110
    Smean = S / buy_sum
    res = Smean * ksi2
    print(Smean)
    print(ksi1)
    print(res)


if __name__ == "__main__":
    test_hypot()
    # main()
