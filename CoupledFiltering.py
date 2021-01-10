import numpy as np


def psf():
    # TODO:: model the filter which is the point spread function  H(X)
    # 1. The PSF size is determined by the sigma and voxel size. It is much smaller than the image.
    # 2. It is easier to use Gaussian-weighted cosine function. (Coupled filtering #1 p.437, formula 7)
    None


def apply(image, psf_filter):  # assume the filter is a P*P array where P is a odd number
    psf_filter = np.fliplr(np.flipud(psf_filter))
    padding = int(psf_filter.shape[0] // 2)
    imagePadded = np.zeros([image.shape[0] + 2 * padding, image.shape[1] + 2 * padding])
    imagePadded[padding: imagePadded.shape[0] - padding, padding: imagePadded.shape[1] - padding] = image
    output = np.zeros(image.shape)

    for (y, x) in np.ndindex(image.shape):
        output[y, x] = (imagePadded[y: y + psf_filter.shape[0] - 1, x: x + psf_filter.shape[1] - 1] * psf_filter).sum()
