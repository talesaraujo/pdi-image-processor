import numpy as np
from image_processor import imgio

GRAYSCALE_DOMAIN = (0, 256)

def normalize(img: np.ndarray) -> np.ndarray:
    """Normalizes the entry image to the decimal unit range."""
    return img / 255.0


def set_brightness(img: np.ndarray, factor: int) -> np.ndarray:
    """Controls the image brightness through a certain numeric factor."""
    return factor * img


def negative(img: np.ndarray) -> np.ndarray:
    """Returns the image values inversed."""
    return 1 - img


def log_transform(img: np.ndarray, c: int) -> np.ndarray:
    """Applies the logarithmic transformation over the input image."""
    return c * np.log(1 + img)


def gamma_transform(img: np.ndarray, c: int, gamma: float) -> np.ndarray:
    """Applies the gamma transformation over the input image."""
    return c * (img ** gamma)


def rescale(img: np.ndarray) -> np.ndarray:
    """Rescales the image to fit the [0, 1] interval. It will make the image
    appear with a greyish tone."""
    img += np.abs(np.min(img))
    img /= np.max(img)
    return img


def interpolate_points(pa: tuple, pb: tuple) -> None:
    """Returns the A and b coefficients that represent a linear function."""
    if len(pa) != len(pb) != 2:
        raise ValueError("Point tuples must have length of 2.")
    
    if pb[0] <= pa[0]:
        raise ValueError("The first value of x is supposed to be lower than the second one.")
    
    for i in range(2):
        if not np.all([pa[i] >= 0, pb[i] >= 0]):
            raise ValueError("Axes are not allowed to hold negative values.")

        if not np.all([pa[i] < 256, pb[i] < 256]):
            raise ValueError("Axes are not allowed to hold values greater than 255.")

    A = (pa[1] / (pa[0] - pb[0])) + (pb[1] / (pb[0] - pa[0]))
    b = ((-pa[1] * pb[0]) / (pa[0] - pb[0])) + ((-pb[1]*pa[0]) / ( pb[0] - pa[0]))

    return A, b


def linear_piecewise(img: np.ndarray, pa: tuple, pb: tuple, plot=False) -> np.ndarray:
    """Returns the processed image according to the linear interpolation function defined by two points."""
    for value in [*pa, *pb]:
        if value in [0, 1, 254, 255]:
            raise ValueError("Line bounds too restrictive. Acceptable values: 2 to 253")
    
    line_0 = [(0,0), tuple([p - 1 for p in pa])]
    line_1 = [pa, pb]
    line_2 = [tuple([p + 1 for p in pb]), (255, 255)]

    coeficients_0 = interpolate_points(*line_0)
    coeficients_1 = interpolate_points(*line_1)
    coeficients_2 = interpolate_points(*line_2)

    domain_0 = np.arange(GRAYSCALE_DOMAIN[0], pa[0])
    domain_1 = np.arange(pa[0], pb[0])
    domain_2 = np.arange(pb[0], GRAYSCALE_DOMAIN[1])

    general_domain = np.arange(0, 256)

    output_0 = coeficients_0[0]*domain_0 + coeficients_0[1]
    output_1 = coeficients_1[0]*domain_1 + coeficients_1[1]
    output_2 = coeficients_2[0]*domain_2 + coeficients_2[1]

    general_output = [*output_0, *output_1, *output_2]

    assert len(domain_0) == len(output_0)
    assert len(domain_1) == len(output_1)
    assert len(domain_2) == len(output_2)
    assert len(general_domain) == len(general_output)

    if plot:
        imgio.plot_interpolation_function(img, pa, pb, general_output)

    img_p = np.array(img, copy=True)

    for row in range(img.shape[0]):
        for col in range(img.shape[1]):
            img_p[row, col] = general_output[img_p[row, col]]
        
    return img_p
