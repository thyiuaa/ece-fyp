import numpy as np

import AffineWarping

affine_test_X = np.arange(81).reshape((9, 9))


def translation_test(X, T0, T1):
    print("After translation (", T0, ",", T1, "):")
    print(AffineWarping.translation(X, [T0, T1]))
    print()


print("===== START of testing translation =====")
print("Before translation:")
print(affine_test_X, "\n")
translation_test(affine_test_X, 0, 0)
translation_test(affine_test_X, 1, 4)
translation_test(affine_test_X, 1, -4)
translation_test(affine_test_X, 5, 1)
translation_test(affine_test_X, -5, 1)
print("^^^^^ END of testing translation ^^^^^")


def transform_test(X, M00, M01, M10, M11):
    print("After transform (", M00, ",", M01, ",", M10, ",", M11, "):")
    print(AffineWarping.transformation(X, [[M00, M01], [M10, M11]]))
    print()


print("===== START of testing translation =====")
print("Before translation:")
print(affine_test_X, "\n")
transform_test(affine_test_X, 0, 0, 0, 0)
transform_test(affine_test_X, 1, 0, 0, 1)
transform_test(affine_test_X, 1, 0, 0, -1)
transform_test(affine_test_X, 1, 3, 0, 1)
transform_test(affine_test_X, 1, 0, 3, 1)
print("^^^^^ END of testing translation ^^^^^")
