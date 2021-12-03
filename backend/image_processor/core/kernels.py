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

GAUSSIAN_BLUR = np.asarray(a=((np.asanyarray(dtype=np.int8,
    a=[[1, 2, 1],
       [2, 4, 2],
       [1, 2, 1]]
))/16))
