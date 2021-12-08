# Implement thresholding (limizarização)

# Implement the application of a generic filter through convolution

# Average filtering 

import numpy as np
from core import kernels, intensity


def convolve2D(img: np.ndarray, filter: np.ndarray=None, strides: int=1) -> np.ndarray:
    # Apply cross-relation
    filter = np.flipud(np.fliplr(filter))

    # Set dynamic padding
    padding = int(filter.shape[0]/2)

    # Get shapes
    imgsize_x, imgsize_y = img.shape[0], img.shape[1]
    filtersize_x, filtersize_y = filter.shape[0], filter.shape[1]    

    # Shape of output matrix
    outputsize_x = int((imgsize_x - filtersize_x + 2*padding) / strides) + 1
    outputsize_y = int((imgsize_y - filtersize_y + 2*padding) / strides) + 1

    output = np.zeros((outputsize_x, outputsize_y))

    # Applying equal padding to both sides
    if padding != 0:
        img_padded = np.zeros((imgsize_x + (2*padding), imgsize_y + (2*padding)))
        img_padded[padding:-1*padding, padding:-1*padding] = img
    else:
        img_padded = img

    # Actual convolution step    
    for j in range(imgsize_y):

        if j > imgsize_y - filtersize_y:
            break

        if j % strides == 0:
            for i in range(imgsize_x):
                if i > imgsize_x - filtersize_x:
                    break
                try:
                    if i % strides == 0:
                        output[i, j] = (filter * img_padded[i:i+filtersize_x, j:j+filtersize_y]).sum()
                except:
                    break

    return output


def laplacian(img: np.ndarray, rescale=True) -> np.ndarray:
    img_l = convolve2D(img, kernels.LAPLACIAN)
    return intensity.rescale(img_l) if rescale else img_l


def high_boost(img: np.ndarray) -> np.ndarray:
    img_g = convolve2D(img, kernels.GAUSSIAN_BLUR_5x5)
    img_b = img - img_g
    img_p = img + img_b

    return img_p
