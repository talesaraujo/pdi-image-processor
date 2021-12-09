import numpy as np

def normalize(img: np.ndarray) -> np.ndarray:
    return img / 255.0

def set_brightness(img: np.ndarray, factor: int) -> np.ndarray:
    return factor * img

def negative(img: np.ndarray) -> np.ndarray:
    return 1 - img

def log_transform(img: np.ndarray, c: int) -> np.ndarray:
    return c * np.log(1 + img)

def gamma_transform(img: np.ndarray, c: int, gamma: float) -> np.ndarray:
    return c * (img ** gamma)


def rescale(img: np.ndarray) -> np.ndarray:
    img += np.abs(np.min(img))
    img /= np.max(img)
    return img


def interpolate_points(pa: tuple, pb: tuple) -> None:
    """Returns the A and b coefficients that represent a linear function."""
    if len(pa) != len(pb) != 2:
        raise ValueError("Point tuples must have length of 2.")
    
    if pa[0] == pb[0]:
        raise ValueError("The two provided points do not form a function.")

    for i in range(2):
        if not np.all([pa[i] >= 0, pb[i] >= 0]):
            raise ValueError("Axes are not allowed to hold negative values.")

        if not np.all([pa[i] < 256, pb[i] < 256]):
            raise ValueError("Axes are not allowed to hold values greater than 255.")
    

    A = (pa[1] / (pa[0] - pb[0])) + (pb[1] / (pb[0] - pa[0]))
    b = ((-pa[1] * pb[0]) / (pa[0] - pb[0])) + ((-pb[1]*pa[0]) / ( pb[0] - pa[0]))

    return A, b
