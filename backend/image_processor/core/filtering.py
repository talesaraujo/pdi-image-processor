# Implement thresholding (limizarização)

# Implement the application of a generic filter through convolution

# Average filtering 

import numpy as np


def convolve2D(img: np.ndarray, filter: np.ndarray=None, padding: int=1, strides: int=1) -> np.ndarray:
    # Apply cross-relation
    filter = np.flipud(np.fliplr(filter))

    # Get shapes
    imgsize_x, imgsize_y = img.shape[0], img.shape[1]
    filtersize_x, filtersize_y = filter.shape[0], filter.shape[1]    

    # Shape of output matrix
    outputsize_x = int((imgsize_x - filtersize_x + 2*padding) / strides) + 1
    outputsize_y = int((imgsize_y - filtersize_y + 2*padding) / strides) + 1

    output = np.zeros((outputsize_x, outputsize_y))

    print(f"{output}\n")

    # Applying equal padding to both side
    if padding != 0:
        img_padded = np.zeros((imgsize_x + (2*padding), imgsize_y + (2*padding)))
        img_padded[padding:-1*padding, padding:-1*padding] = img
    else:
        img_padded = img

    # Convolution step
    # for j in range(imgsize_y):
    #     if j > imgsize_y - filtersize_y:

    return img_padded
