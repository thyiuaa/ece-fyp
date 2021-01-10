import numpy as np

import AffineWarping

result = open("result.txt", "w")


def affine_warping_test(X, M00, M01, M10, M11, T0, T1):
    result.write(
        "After affine transform (" + str(M00) + "," + str(M01) + "," + str(M10) + "," + str(M11) + ") + (" + str(T0) + "," + str(T1) + "):\n")
    result.write(str(AffineWarping.affine_warping(X, np.array([[M00, M01], [M10, M11]]), np.array([T0, T1]))))
    result.write("\n\n")


affine_test_X = np.arange(81).reshape((9, 9))
result.write("===== START of affine warping test =====\n")
result.write("Before affine warping:\n")
result.write(str(affine_test_X))
result.write("\n\n")
affine_warping_test(affine_test_X, 0, 0, 0, 0, 0, 0)
affine_warping_test(affine_test_X, 1, 0, 0, 1, 0, 0)
result.write("X translation\n")
affine_warping_test(affine_test_X, 1, 0, 0, 1, 3, 0)
affine_warping_test(affine_test_X, 1, 0, 0, 1, -3, 0)
affine_warping_test(affine_test_X, 1, 0, 0, 1, 2.3, 0)
result.write("Y translation\n")
affine_warping_test(affine_test_X, 1, 0, 0, 1, 0, 3)
affine_warping_test(affine_test_X, 1, 0, 0, 1, 0, -3)
affine_warping_test(affine_test_X, 1, 0, 0, 1, 0, 2.3)
result.write("X scaling\n")
affine_warping_test(affine_test_X, 2, 0, 0, 1, 0, 0)
affine_warping_test(affine_test_X, 0.32, 0, 0, 1, 0, 0)
affine_warping_test(affine_test_X, -0.5, 0, 0, 1, 0, 0)
result.write("Y scaling\n")
affine_warping_test(affine_test_X, 1, 0, 0, 2, 0, 0)
affine_warping_test(affine_test_X, 1, 0, 0, 0.32, 0, 0)
affine_warping_test(affine_test_X, 1, 0, 0, -0.5, 0, 0)
result.write("X shearing\n")
affine_warping_test(affine_test_X, 1, 1, 0, 1, 0, 0)
affine_warping_test(affine_test_X, 1, 0.46, 0, 1, 0, 0)
affine_warping_test(affine_test_X, 1, -0.372, 0, 1, 0, 0)
result.write("Y shearing\n")
affine_warping_test(affine_test_X, 1, 0, 1, 1, 0, 0)
affine_warping_test(affine_test_X, 1, 0, 0.46, 1, 0, 0)
affine_warping_test(affine_test_X, 1, 0, -0.372, 1, 0, 0)
result.write("^^^^^ END of affine warping test ^^^^^\n")