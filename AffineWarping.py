import numpy as np


def affine_warping(arr, Mw, Tw):
    """
    :param arr: matrix to be processed
    :param Mw: a 2x2 transformation matrix
    :param Tw: x and y translation factor (+ve: right, up; -ve: left, down)
    :return: A new matrix after affine warping
    Mw = [[1+a, b], [c, 1+d]]
    |Mw| = 1
    a = axial strain
    b = axial shear
    c = lateral shear
    d = lateral strain
    """
    arr = np.flipud(arr)  # flip the array upside down so that bottom left element is the origin
    new_arr = np.zeros(arr.shape)
    for (y, x) in np.ndindex(arr.shape):
        new_x = x * Mw[0, 0] + y * Mw[0, 1] + Tw[0]
        new_y = (arr.shape[0] - 1) - (x * Mw[1, 0] + y * Mw[1, 1] + Tw[1])
        if 0 <= new_y < new_arr.shape[0] and 0 <= new_x < new_arr.shape[1]:
            new_arr[int(new_y), int(new_x)] = arr[y, x]

    return new_arr

# def transformation(X, Mw):
#     """
#     :param X: matrix to be transformed
#     :param Mw: a 2x2 transformation matrix
#     :return: A new matrix after translation
#     """
#     X = np.flipud(X)  # flip the array upside down so that bottom left element is the origin
#     new_X = np.zeros(X.shape)
#     for row in range(X.shape[0]):
#         for col in range(X.shape[1]):
#             new_col = col * Mw[0, 0] + row * Mw[0, 1]
#             new_row = (X.shape[0] - 1) - (col * Mw[1, 0] + row * Mw[1, 1])
#             if 0 <= new_row < new_X.shape[0] and 0 <= new_col < new_X.shape[1]:
#                 new_X[int(new_row), int(new_col)] = X[row, col]
#
#
# def translation(X, Tw):
#     """
#     :param X: matrix to be translated
#     :param Tw: x and y translation factor (+ve: right, up; -ve: left, down)
#     :return: A new matrix after translation
#     """
#     # vertical translation
#     if Tw[1] == 0:
#         new_X = X
#     else:
#         new_X = np.roll(X, -Tw[1], 0)  # negate the sign to fit index representation
#         empty_rows = np.zeros(X[:abs(Tw[1])].shape)  # prepare empty rows for insert
#         if Tw[1] < 0:
#             new_X[:-Tw[1]] = empty_rows
#         else:
#             new_X[-Tw[1]:] = empty_rows
#
#     # horizontal translation
#     if Tw[0] == 0:
#         None
#     else:
#         Tw0_range = range(abs(Tw[0]))
#         if Tw[0] < 0:  # do less checking if put outside of loop
#             for i in range(new_X.shape[0]):  # [1 2 3 4 5] => [0 0 3 4 5] => [3 4 5 0 0]
#                 for _ in Tw0_range: new_X[i, _] = 0
#                 new_X[i] = np.roll(new_X[i], Tw[0], 0)
#         else:
#             for i in range(new_X.shape[0]):  # [1 2 3 4 5] => [4 5 1 2 3] => [0 0 1 2 3]
#                 new_X[i] = np.roll(new_X[i], Tw[0], 0)
#                 for _ in Tw0_range: new_X[i, _] = 0
#
#     return new_X
