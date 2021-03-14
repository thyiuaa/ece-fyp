import numpy as np
import matplotlib.pyplot as plt
import os, sys, inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(1, parent_dir)

import AffineWarping
import CoupledFiltering


def affine_warping_test(X, M00, M01, M10, M11, T0, T1, result):
    result.write("After affine transform (" + str(M00) + "," + str(M01) + "," + str(M10) + "," + str(M11) + ") + (" + str(T0) + "," + str(T1) + "):\n")
    result.write(str(AffineWarping.affine_warping(X, np.array([[M00, M01], [M10, M11]]), np.array([T0, T1]))))
    result.write("\n\n")


def run_affine_warping():
    if not os.path.exists("result"):
        os.mkdir("result")
    result = open("result/affine_warping_test_result.txt", "w")
    affine_test_X = np.arange(81).reshape((9, 9))
    result.write("===== START of affine warping test =====\n")
    result.write("Before affine warping:\n")
    result.write(str(affine_test_X))
    result.write("\n\n")
    affine_warping_test(affine_test_X, 0, 0, 0, 0, 0, 0, result)
    affine_warping_test(affine_test_X, 1, 0, 0, 1, 0, 0, result)
    result.write("X translation\n")
    affine_warping_test(affine_test_X, 1, 0, 0, 1, 3, 0, result)
    affine_warping_test(affine_test_X, 1, 0, 0, 1, -3, 0, result)
    affine_warping_test(affine_test_X, 1, 0, 0, 1, 2.3, 0, result)
    result.write("Y translation\n")
    affine_warping_test(affine_test_X, 1, 0, 0, 1, 0, 3, result)
    affine_warping_test(affine_test_X, 1, 0, 0, 1, 0, -3, result)
    affine_warping_test(affine_test_X, 1, 0, 0, 1, 0, 2.3, result)
    result.write("X scaling\n")
    affine_warping_test(affine_test_X, 2, 0, 0, 1, 0, 0, result)
    affine_warping_test(affine_test_X, 0.32, 0, 0, 1, 0, 0, result)
    affine_warping_test(affine_test_X, -0.5, 0, 0, 1, 0, 0, result)
    result.write("Y scaling\n")
    affine_warping_test(affine_test_X, 1, 0, 0, 2, 0, 0, result)
    affine_warping_test(affine_test_X, 1, 0, 0, 0.32, 0, 0, result)
    affine_warping_test(affine_test_X, 1, 0, 0, -0.5, 0, 0, result)
    result.write("X shearing\n")
    affine_warping_test(affine_test_X, 1, 1, 0, 1, 0, 0, result)
    affine_warping_test(affine_test_X, 1, 0.46, 0, 1, 0, 0, result)
    affine_warping_test(affine_test_X, 1, -0.372, 0, 1, 0, 0, result)
    result.write("Y shearing\n")
    affine_warping_test(affine_test_X, 1, 0, 1, 1, 0, 0, result)
    affine_warping_test(affine_test_X, 1, 0, 0.46, 1, 0, 0, result)
    affine_warping_test(affine_test_X, 1, 0, -0.372, 1, 0, 0, result)
    result.write("^^^^^ END of affine warping test ^^^^^\n")
    result.close()


def run_psf():
    np.set_printoptions(linewidth=1000)
    if not os.path.exists("result"):
        os.mkdir("result")

    psf = CoupledFiltering.psf()
    result = open("result/psf_test_result.txt", "w")
    result.write(str(psf))
    result.close()
    fig, ax = plt.subplots()
    c = ax.pcolormesh(psf)
    ax.set_title('PSF')
    fig.colorbar(c, ax=ax)
    fig.tight_layout()
    plt.show()


def run_coupled_filtering():
    np.set_printoptions(linewidth=1000)
    if not os.path.exists("result"):
        os.mkdir("result")

    result = open("result/coupled_filtering_test_result.txt", "w")
    test_image = np.loadtxt("test_image.dat")
    test_filter = np.loadtxt("test_filter.dat")
    result.write(str(CoupledFiltering.apply(test_image, test_filter)))
    result.close()
    # compare this result with the result from running "test_run_coupled_filtering_octave.m" in octave (a open source matlab like software)
    # a = np.loadtxt("coupled_filtering_test_result_octave.txt")
    # b = CoupledFiltering.apply(test_image, test_filter)
    # print(a-b)