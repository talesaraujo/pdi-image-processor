# TODO: Implement thresholding (limizarização)!!!
import numpy as np
from image_processor import imgio
from image_processor.core import kernels, intensity
from skimage import filters
from skimage.morphology import disk


def convolve2D(img: np.ndarray, filter: np.ndarray=None, strides: int=1) -> np.ndarray:
    """Applies the two-dimentional convolution with a certain mask (filter).
    
    In order to prevent image shrinking, this algorithm fills extra values with zeros,
    so that the output image will have darkened borders. 
    """
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
    """Returns the image with its borders highlighted (by Laplacian filter)."""
    img_l = convolve2D(img, kernels.LAPLACIAN)
    return intensity.rescale(img_l) if rescale else img_l


def high_boost(img: np.ndarray) -> np.ndarray:
    """Improves the image via High-Boost processing (by using the Gaussian Filter)."""
    img_g = convolve2D(img, kernels.GAUSSIAN_BLUR_5x5)
    img_b = img - img_g
    img_p = img + img_b

    return img_p


def dft(x: np.ndarray) -> np.ndarray:
    """Computes the Discrete Fourier Transform by using the naive approach
    (a direct formula application, which resolves at O(n^2) time)
    
    Parameters
    ----------
    x : np.ndarray
        The 1-dimentional array from which the transform will be calculated from.

    Returns
    -------
    X: np.ndarray
        The value of the frequencies computed for the x array.
    """
    N = len(x)
    X = []

    # Iterate k through 0..N-1
    for k in range(N):
        sum_ = complex(0)
        # Iterate n through 0..N-1
        for n in range(N):
            sum_ += x[n] * np.exp(complex(-2j * k * n * np.pi) / N)
        X.append(sum_)

    return np.asarray(X)


def dft2(f: np.ndarray) -> np.ndarray:
    """Computes the 2-Dimentional Discrete Fourier Transform by using the naive
    approach (a direct formula application, which resolves at O(n^2) time)
    
    Parameters
    ----------
    f : np.ndarray
        The 2-dimentional array from which the transform will be calculated from.

    Returns
    -------
    F: np.ndarray
        The value of the frequencies computed for the f array.
    """
    M, N = f.shape

    F = np.zeros((M,N), complex)

    for u in range(M):
        for v in range(N):
            for x in range(M):
                for y in range(N):
                    F[u, v] += f[x, y] * np.exp(-2j * np.pi * ((u*x / M) + (v*y / N)))

    return F


def idft2(F: np.ndarray) -> np.ndarray:
    """Computes the 2-Dimentional Inverse Discrete Fourier Transform by using 
    the naive approach (a direct formula application, which resolves at O(n^2) time)
    
    Parameters
    ----------
    F : np.ndarray
        The 2-dimentional array from which the inverse transform will be 
        calculated from.

    Returns
    -------
    F: np.ndarray
        The value of the frequencies computed for the f array.
    """
    M, N = F.shape

    f = np.zeros((M,N), complex)

    for x in range(M):
        for y in range(N):
            for u in range(M):
                for v in range(N):
                    f[x, y] += (1 / (M * N)) * F[u, v] * np.exp(2j * np.pi * ((u*x / M) + (v*y / N)))

    return f


def get_circular_filter(radius: int, negative: bool=False, gaussian: bool=False, sigma: float=3) -> np.ndarray:
    """Creates a circular image, with a steep or smooth color shifting.
    
    If the image is supposed to have a radius of R, the output will have 
    dimensions of R+1 x R+1 elements.
    """
    disk_filter = disk(radius)
    
    if negative:
        disk_filter = intensity.negative(disk_filter)

    disk_filter *= 255

    if gaussian:
        disk_filter = filters.gaussian(disk_filter, sigma=sigma)

    return disk_filter


def gen_image_filter(img_source: np.ndarray, radius: int, negative: bool=False, gaussian: bool=False, sigma: float=3) -> np.ndarray:
    """Generates a circular filter that is exactly the same size as the image."""
    circular_filter = get_circular_filter(radius, negative, gaussian, sigma)
    complete_filter = np.ones(img_source.shape) if negative else np.zeros(img_source.shape)

    half_shape = tuple(np.array(img_source.shape) / 2)
    half_shape = tuple(np.int(np.floor(value)) for value in half_shape)

    complete_filter[
        half_shape[0]-radius:half_shape[0]+radius+1,
        half_shape[1]-radius:half_shape[1]+radius+1
    ] = circular_filter

    return complete_filter


def apply_frequency_filtering(img: np.ndarray, filter_type: str, radius: int, gaussian: bool=False, std: float=3) -> None:
    """Applies the fourier transform.

    Parameters
    ----------
    img : np.ndarray
        The image.
    filter_type : str in { 'low', 'high' }
        The desired filter (low-pass or high-pass).
    
    NOTE: The image is supposed to be normalized [0..1]
    """
    if img.max() > 1:
        img = intensity.normalize(img)

    # ONWARDS STEP: Fourier Transform
    if img.shape[0] <= 32:
        # Apply my transform
        img_t = dft2(img)
    
    else:
        # Image too large, use np-fft instead
        img_t = np.fft.fft2(img)
    
    # Visualization of Fourier Transform
    img_t = np.fft.fftshift(img_t) # Shift frequencies to origin
    img_t_vis = np.abs(img_t) # Generate visualization
    img_t_vis[img_t_vis  > 2000] = 2000 # Cut off extreme values
    img_t_vis = intensity.rescale(img_t_vis) # Avoid negative values
    imgio.display(img_t_vis)
    print(img_t_vis.max(), img_t_vis.min())

    if filter_type == 'low':
        complete_filter = gen_image_filter(
            img_source=img_t,
            radius=radius,
            negative=False,
            gaussian=True,
            sigma=std
        )
    
    if filter_type == 'high':
        complete_filter = gen_image_filter(
            img_source=img_t,
            radius=radius,
            negative=True,
            gaussian=gaussian,
            sigma=std
        )

    # Display selected filter
    imgio.display(complete_filter)

    # Actually apply the filter on the image
    img_t_proc = np.multiply(img_t, complete_filter)

    # Display Processed Transformed Image (abs value)
    img_t_proc_vis = np.abs(img_t_proc)
    # Cut off extreme values
    img_t_proc_vis[img_t_proc_vis > 1000] = 1000

    # BACKWARS STEP: Inverse Transform
    img_t_proc = np.fft.ifftshift(img_t_proc)
    img_proc = np.fft.ifft2(img_t_proc)

    # Visualization of the processed image
    img_proc_d = np.real(img_proc)
    img_proc_d = intensity.rescale(img_proc_d)

    # imgio.display(img_proc_d)

    return img_proc_d
