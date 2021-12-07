import numpy as np


def histogram(img: np.ndarray, L: int=256) -> np.ndarray:
    hist = np.zeros(L, dtype=np.int64)

    for element in img.flatten():
        hist[element] += 1

    return hist


def histogram_normalized(img: np.ndarray, L: int=256, plot: bool=False) -> np.ndarray:
    hist = np.zeros(L, dtype=np.float)

    for element in img.flatten():
        hist[element] += 1

    normalized_hist = hist / (img.shape[0] * img.shape[1])

    return normalized_hist


def cumulative_probability(normalized_hist: np.ndarray) -> np.ndarray:
    cumulative_prob = np.array(normalized_hist, copy=True)

    for i in range(len(cumulative_prob)):
        if i != (len(cumulative_prob) - 1):
            cumulative_prob[i+1] = cumulative_prob[i] + cumulative_prob[i+1]

    return cumulative_prob


def remap_shade_values(cumulative_prob: np.ndarray, L: int=256) -> None:
    new_intensity_levels = np.zeros(L, np.int64)

    for i in range(len(cumulative_prob)):
        new_intensity_levels[i] = np.ceil(cumulative_prob[i] * (L - 1))

    return new_intensity_levels


def equalize_histogram(img: np.ndarray) -> np.ndarray:
    normalized_hist = histogram_normalized(img=img, plot=False)
    cumulative_prob = cumulative_probability(normalized_hist)
    remapped_values = remap_shade_values(cumulative_prob)

    for row in range(img.shape[0]):
        for col in range(img.shape[1]):
            img[row, col] = remapped_values[img[row,col]]
    
    return img
