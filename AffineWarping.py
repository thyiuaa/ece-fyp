import numpy as np


def affine_warping(arr, M, T, window = None, height = 0, width = 0):
    """
    :param arr: matrix of original data
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
    if window != None:  # arr should be the whole image
        new_height = int(np.round(width * np.abs(M[1, 0]) + height * np.abs(M[1, 1])))
        new_width = int(np.round(width * np.abs(M[0, 0]) + height * np.abs(M[0, 1])))
        new_arr = np.zeros([new_height, new_width])
        for y in range(window.y, window.y+height):
            for x in range(window.x, window.x+width):
                new_y = int(x * M[1, 0] + y * M[1, 1] - T[1])  # T[1] < 0: down, > 0: up
                new_x = int(x * M[0, 0] + y * M[0, 1] + T[0])
                if new_y < y or new_x < x: continue
                new_arr[new_y - y, new_x - x] = arr[new_y, new_x]
    else:
        arr = np.flipud(arr)  # flip the array upside down so that bottom left element is the origin
        new_height = int(np.round(arr.shape[1] * np.abs(M[1, 0]) + arr.shape[0] * np.abs(M[1, 1])))
        new_width = int(np.round(arr.shape[1] * np.abs(M[0, 0]) + arr.shape[0] * np.abs(M[0, 1])))
        new_arr = np.zeros([new_height, new_width])
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
