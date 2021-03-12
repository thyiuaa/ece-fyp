import math

import numpy as np

def psf():
    s_x = 12
    s_y = 8
    width = 100  # PSF width
    height = 100  # PSF height
    freq = 2*(3e6)/1540/1000 # ref #33 p.406
    output = np.empty([height, width])
    for y in range(-height // 2, height // 2):
        for x in range(-width // 2, width // 2):
            cos_function = math.cos(2 * math.pi * freq * x)
            output[y + height // 2, x + width // 2] = math.exp(-0.5 * ((x * x) / (s_x * s_x) + (y * y) / (s_y * s_y))) * cos_function
    return output


def apply(image, psf_filter):  # do convolution and take the center part, same as https://octave.sourceforge.io/octave/function/conv2.html with shape="same"
    # start_y = psf_filter.shape[0] // 2
    # start_x = psf_filter.shape[1] // 2
    # result = np.zeros(image.shape)
    # for j in range(start_y, start_y + result.shape[0]):
    #     for i in range(start_x, start_x + result.shape[1]):
    #         for b in range(0, image.shape[0]):
    #             for a in range(0, image.shape[1]):
    #                 if (-1 < i - a < psf_filter.shape[1]) and (-1 < j - b < psf_filter.shape[0]):
    #                     result[j - start_y, i - start_x] += image[b, a] * psf_filter[j - b, i - a]
    new_shape = np.array(image.shape)+np.array(psf_filter.shape)-1
    padded_image = np.zeros(new_shape)
    padded_psf_filter = np.zeros(new_shape)
    
    padded_image[0:image.shape[0], 0:image.shape[1]] = image
    padded_psf_filter[0:psf_filter.shape[0], 0:psf_filter.shape[1]] = psf_filter

    image_padding = np.intc(np.ceil((np.array(psf_filter.shape)-1)/2))
    result = np.fft.ifft2(np.fft.fft2(padded_image) * np.fft.fft2(padded_psf_filter))[image_padding[0]:image_padding[0]+image.shape[0], image_padding[1]:image_padding[1]+image.shape[1]]
    return np.real(result)
