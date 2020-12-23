import numpy as np

import AffineWarping

affine_test_X = np.arange(81).reshape((9, 9))


def translation_test(X, T0, T1):
    print("After translation (", T0, ",", T1, "):")
    print(AffineWarping.translation(X, [T0, T1]))
    print()


# def transform_test(X, M00, M01, M10, M11):
#     print("After transform (", M00, ",", M01, ",", M10, ",", M11, "):")
#     print(AffineWarping.transformation(X, [[M00, M01], [M10, M11]]))
#     print()


def affine_warping_test(X, M00, M01, M10, M11, T0, T1):
    print("After affine transform (", M00, ",", M01, ",", M10, ",", M11, ") + (", T0, ",", T1, "):")
    print(AffineWarping.affine_warping(X, [[M00, M01], [M10, M11]], [T0, T1]))
    print()


print("===== START of translation test =====")
print("Before translation:")
print(affine_test_X, "\n")
translation_test(affine_test_X, 0, 0)
translation_test(affine_test_X, 1, 4)
translation_test(affine_test_X, 1, -4)
translation_test(affine_test_X, 5, 1)
translation_test(affine_test_X, -5, 1)
print("^^^^^ END of translation test ^^^^^")

# print("===== START of transformation test =====")
# print("Before transformation:")
# print(affine_test_X, "\n")
# transform_test(affine_test_X, 0, 0, 0, 0)
# transform_test(affine_test_X, 1, 0, 0, 1)
# transform_test(affine_test_X, 2, 0, 0, 1)
# transform_test(affine_test_X, 1, 0, 0, 2)
# transform_test(affine_test_X, -1, 0, 0, 1)
# transform_test(affine_test_X, 1, 0, 0, -1)
# transform_test(affine_test_X, 1, 1, 0, 1)
# transform_test(affine_test_X, 1, -1, 0, 1)
# transform_test(affine_test_X, 1, 0, 1, 1)
# transform_test(affine_test_X, 1, 0, -1, 1)
# print("^^^^^ END of transformation test ^^^^^")

print("===== START of affine warping test =====")
print("Before affine warping:")
print(affine_test_X, "\n")
affine_warping_test(affine_test_X, 0, 0, 0, 0, 0, 0)
affine_warping_test(affine_test_X, 1, 0, 0, 1, 3, 3)
affine_warping_test(affine_test_X, 2, 0, 0, 1, 1, 1)
affine_warping_test(affine_test_X, 1, 0, 0, 2, 0, -3)
affine_warping_test(affine_test_X, -1, 0, 0, 1, 0, 3)
affine_warping_test(affine_test_X, 1, 0, 0, -1, 2, 0)
affine_warping_test(affine_test_X, 1, 1, 0, 1, -2, 0)
affine_warping_test(affine_test_X, 1, -1, 0, 1, 0, 0)
affine_warping_test(affine_test_X, 1, 0, 1, 1, 0, -3)
affine_warping_test(affine_test_X, 1, 0, -1, 1, 0, 3)
print("^^^^^ END of affine warping test ^^^^^")
