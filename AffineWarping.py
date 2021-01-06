from typing import List

import numpy as np


# def transformation(X: np.ndarray, Mw: List[List[int]]) -> np.ndarray:
#     """
#     :param X: matrix to be transformed
#     :param Mw: a 2x2 transformation matrix
#     :return: A new matrix after translation
#     """
#     if Mw == [[0, 0], [0, 0]]:  # no operation
#         return np.zeros(X.shape)
#     elif Mw == [[1, 0], [0, 1]]:  # identity
#         return X
#     else:
#         X = np.flip(X, 0)
#         new_X = np.zeros(X.shape)
#         for row in range(X.shape[0]):
#             for col in range(X.shape[1]):
#                 new_col = col * Mw[0][0] + row * Mw[0][1]
#                 new_row = X.shape[0]-1-(col * Mw[1][0] + row * Mw[1][1])
#                 if 0 <= new_row < new_X.shape[0] and 0 <= new_col < new_X.shape[1]:
#                     new_X[new_row][new_col] = X[row][col]
#
#         return new_X


def translation(X: np.ndarray, Tw: List[int]) -> np.ndarray:
    """
    :param X: matrix to be translated
    :param Tw: x and y translation factor (+ve: right, up; -ve: left, down)
    :return: A new matrix after translation
    """
    # vertical translation
    if Tw[1] == 0:
        new_X = X
    else:
        new_X = np.roll(X, -Tw[1], 0)  # negate the sign to fit index representation
        empty_rows = np.zeros(X[:abs(Tw[1])].shape)  # prepare empty rows for insert
        if Tw[1] < 0:
            new_X[:-Tw[1]] = empty_rows
        else:
            new_X[-Tw[1]:] = empty_rows

    # horizontal translation
    if Tw[0] == 0:
        None
    else:
        Tw0_range = range(abs(Tw[0]))
        if Tw[0] < 0:  # do less checking if put outside of loop
            for i in range(new_X.shape[0]):  # [1 2 3 4 5] => [0 0 3 4 5] => [3 4 5 0 0]
                for _ in Tw0_range: new_X[i][_] = 0
                new_X[i] = np.roll(new_X[i], Tw[0], 0)
        else:
            for i in range(new_X.shape[0]):  # [1 2 3 4 5] => [4 5 1 2 3] => [0 0 1 2 3]
                new_X[i] = np.roll(new_X[i], Tw[0], 0)
                for _ in Tw0_range: new_X[i][_] = 0

    return new_X


def affine_warping(X: np.ndarray, Mw: List[List[int]], Tw: List[int]) -> np.ndarray:
    """
    :param X: matrix to be processed
    :param Mw: a 2x2 transformation matrix
    :param Tw: x and y translation factor (+ve: right, up; -ve: left, down)
    :return: A new matrix after affine warping
    """
    # TODO: Mw accepts float input?
    if Mw == [[0, 0], [0, 0]]:  # no operation
        return np.zeros(X.shape)
    elif Mw == [[1, 0], [0, 1]]:  # identity
        return translation(X, Tw)
    else:
        X = np.flip(X, 0)
        new_X = np.zeros(X.shape)
        for row in range(X.shape[0]):
            for col in range(X.shape[1]):
                new_col = col * Mw[0][0] + row * Mw[0][1] + Tw[0]
                new_row = X.shape[0]-1-(col * Mw[1][0] + row * Mw[1][1]) - Tw[1]
                if 0 <= new_row < new_X.shape[0] and 0 <= new_col < new_X.shape[1]:
                    new_X[new_row][new_col] = X[row][col]

        return new_X
