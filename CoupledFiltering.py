import math

import numpy as np


def psf():
    s_x = (0.6 / 2.35)  # TODO:: 0.6*20? (p.442)
    s_y = (1.6 / 2.35)  # TODO:: 1.6*5?
    freq = 3.9  # ref #33 p.406
    output = np.empty([s_y, s_x])
    for y in range(int(-s_y // 2), int(s_y // 2)):  # TODO:: remove int() if possible
        for x in range(int(-s_x // 2), int(s_x // 2)):
            cos_function = math.cos(2 * math.pi * freq * x)
            output[y + s_y // 2, x + s_x // 2] = math.exp(-0.5 * ((x * x) / s_x * s_x + (y * y) / s_y * s_y)) * cos_function
    return output


def apply(image, psf_filter):  # do convolution and take the center part, same as https://octave.sourceforge.io/octave/function/conv2.html with shape="same"
    start_y = psf_filter.shape[0] // 2
    start_x = psf_filter.shape[1] // 2
    result = np.zeros(image.shape)
    for j in range(start_y, start_y + result.shape[0]):
        for i in range(start_x, start_x + result.shape[1]):
            for b in range(0, image.shape[0]):
                for a in range(0, image.shape[1]):
                    if (-1 < i - a < psf_filter.shape[1]) and (-1 < j - b < psf_filter.shape[0]):
                        result[j - start_y, i - start_x] += image[b, a] * psf_filter[j - b, i - a]
    return result
