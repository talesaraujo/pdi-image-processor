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

    hist = hist / (img.shape[0] * img.shape[1])
    cumulative_hist = np.array(hist, copy=True)

    for i in range(len(cumulative_hist)):
        if i != (len(cumulative_hist)-1):
            cumulative_hist[i+1] = cumulative_hist[i] + cumulative_hist[i+1]

    if plot:
        plt.figure(figsize=(18,5))
        plt.xlim(0, 255)
        ax1 = plt.subplot(121)
        ax1.bar(
            x=grayscale_levels,
            height=hist,
            color='gray',
        )
        ax1.set_title('Histogram')
        ax2 = plt.subplot(122)
        ax2.plot(
            grayscale_levels,
            cumulative_hist,
            color='blue',
        )
        ax2.set_title('Cumulative Histogram')
        plt.show()

    return hist
