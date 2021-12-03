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
