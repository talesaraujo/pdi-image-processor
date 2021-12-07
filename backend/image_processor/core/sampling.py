import numpy as np
import matplotlib.pyplot as plt

def histogram(img: np.ndarray, L: int=256, plot: bool=False) -> np.ndarray:
    hist = np.zeros(L, dtype=np.int64)
    grayscale_levels = np.arange(0, L)

    for element in img.flatten():
        hist[element] += 1

    if plot:
        plt.figure(figsize=(8,6))
        plt.bar(
            x=grayscale_levels,
            height=hist,
            color='gray'
        )
        plt.title(f"Image Histogram")
        plt.xlabel("Grayscale level")
        plt.ylabel("Pixel count")
        plt.show()

    return hist


def histogram_normalized(img: np.ndarray, L: int=256, plot: bool=False) -> np.ndarray:
    hist = np.zeros(L, dtype=np.float)
    grayscale_levels = np.arange(0, L)

    for element in img.flatten():
        hist[element] += 1

    normalized_hist = hist / (img.shape[0] * img.shape[1])
    cumulative_prob = cumulative_probability(hist)

    # for value in cumulative_prob:
    #     print(f"{value:.5f}")

    if plot:
        plt.figure(figsize=(18,5))
        plt.xlim(0, 255)
        ax1 = plt.subplot(121)
        ax1.bar(
            x=grayscale_levels,
            height=hist,
            color='gray',
        )
        ax1.set_title('Probabilistic Histogram')
        ax2 = plt.subplot(122)
        ax2.plot(
            grayscale_levels,
            cumulative_prob,
            color='blue',
        )
        ax2.set_title('Cumulative Probability')
        plt.show()

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
