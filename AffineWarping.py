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
