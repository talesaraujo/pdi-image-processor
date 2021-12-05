import numpy as np
import matplotlib.pyplot as plt

def histogram(img: np.ndarray, L: int=256, plot=False) -> np.ndarray:
    hist = np.zeros(L, dtype=np.int)

    for element in img.flatten():
        hist[element] += 1

    if plot:
        plt.figure(figsize=(8,6))
        plt.bar(
            x=np.arange(0, L),
            height=hist,
            color='gray'
        )
        plt.title(f"Image Histogram")
        plt.xlabel("Grayscale level")
        plt.ylabel("Pixel count")
        plt.show()

    return hist
