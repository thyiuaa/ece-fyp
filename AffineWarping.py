import numpy as np


def affine_warping(arr, M, T):
    """
    :param arr: matrix to be processed
    :param M: a 2x2 transformation matrix
    :param T: x and y translation factor (+ve: right, up; -ve: left, down)
    :return: A new matrix after affine warping
    M = [[1+a, b], [c, 1+d]]
    |M| = 1
    a = axial strain
    b = axial shear
    c = lateral shear
    d = lateral strain
    """
    arr = np.flipud(arr)  # flip the array upside down so that bottom left element is the origin
    new_height = int(np.round(arr.shape[1] * np.abs(M[1, 0]) + arr.shape[0] * np.abs(M[1, 1])))  # + np.abs(T[1])))
    new_width = int(np.round(arr.shape[1] * np.abs(M[0, 0]) + arr.shape[0] * np.abs(M[0, 1])))  # + np.abs(T[0])))
    new_arr = np.zeros([new_height, new_width])
    # new_arr = np.zeros(arr.shape)
    for (y, x) in np.ndindex(arr.shape):
        if M[1, 0] < 0:
            new_y = (arr.shape[0] - 1) - (x * M[1, 0] + y * M[1, 1] + T[1])
        else:
            new_y = (new_arr.shape[0] - 1) - (x * M[1, 0] + y * M[1, 1] + T[1])

        if M[0, 1] < 0:
            new_x = (arr.shape[1] - 1) - (x * M[0, 0] + y * M[0, 1] + T[0])
        else:
            new_x = x * M[0, 0] + y * M[0, 1] + T[0]
        if 0 <= new_y < new_arr.shape[0] and 0 <= new_x < new_arr.shape[1]:
            new_arr[int(new_y), int(new_x)] = arr[y, x]

    return new_arr
