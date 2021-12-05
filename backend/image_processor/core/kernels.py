import numpy as np

IDENTITY = np.asanyarray(dtype=np.int8,
    a=[[0, 0, 0],
       [0, 1, 0],
       [0, 0, 0]]
)

EDGE_DETECTION = np.asarray(dtype=np.int8,
    a=[[ 0, -1,  0],
       [-1,  4, -1],
       [ 0, -1,  0]]
)

SHARPEN = np.asarray(dtype=np.int8,
    a=[[ 0, -1,  0],
       [-1,  5, -1],
       [ 0, -1,  0]]
)

BOX_BLUR = np.asarray(a=((np.asanyarray(dtype=np.int8,
    a=[[1, 1,  1],
       [1, 1,  1],
       [1, 1,  1]]
))/9))

GAUSSIAN_BLUR_3x3 = np.asarray(a=((np.asanyarray(dtype=np.int8,
    a=[[1, 2, 1],
       [2, 8, 2],
       [1, 2, 1]]
))/16))


GAUSSIAN_BLUR_5x5 = np.asarray(a=((np.asanyarray(dtype=np.int8,
    a=[[1,  4,  6,  4, 1],
       [4, 16, 24, 16, 4],
       [6, 24, 36, 24, 6],
       [4, 16, 24, 16, 4],
       [1,  4,  6,  4, 1]]
))/256))

GAUSSIAN_BLUR_7x7 = np.asarray(a=((np.asanyarray(dtype=np.int8,
    a=[[  1,   6,  15,  20,  15,   6,  1],
       [  6,  36,  90, 120,  90,  36,  6],
       [ 15,  90, 225, 300, 225,  90, 15],
       [ 20, 120, 300, 400, 300, 120, 20],
       [ 15,  90, 225, 300, 225,  90, 15],
       [  6,  36,  90, 120,  90,  36,  6],
       [  1,   6,  15,  20,  15,   6,  1]]
))/4096))

AVERAGE_SMOOTHED = np.asarray(a=((np.asanyarray(dtype=np.int8,
    a=[[1, 1, 1],
       [1, 1, 1],
       [1, 1, 1]]
))/9))


WEIGHTED_AVERAGE_SMOOTHED = np.asarray(a=((np.asanyarray(dtype=np.int8,
    a=[[1, 2, 1],
       [2, 4, 2],
       [1, 2, 1]]
))/16))
