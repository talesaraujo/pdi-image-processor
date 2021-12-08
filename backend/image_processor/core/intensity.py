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
    if len(pa) != len(pb) != 2:
        raise ValueError("Point tuples must have length of 2.")

    for i in range(2):
        if not np.all([pa[i] >= 0, pb[i] >= 0]):
            raise ValueError("Axes are not allowed to hold negative values.")

        if not np.all([pa[i] < 256, pb[i] < 256]):
            raise ValueError("Axes are not allowed to hold values greater than 255.")
        
        if not pa[i] < pb[i]:
            raise ValueError(f"First point on axis-{i} is supposed to be lower than second one.")

    # TODO: Perform actual interpolation
    
    # domain = np.arange(0, 256)
    # print(domain)
