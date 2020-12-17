from typing import List

import numpy as np



def transformation(X: List[float], Mw: List[float]) -> List[float]:
    None # TODO: implement transformation



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


def affine_warping(X: np.ndarray, Mw: List[int], Tw: List[int]) -> np.ndarray:
    return translation(transformation(X, Tw), Mw)
