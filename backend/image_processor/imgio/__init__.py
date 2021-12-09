import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

from core import sampling

GRAYSCALE_DOMAIN = (0, 255)


def display_image(img: np.ndarray, label: str="Image") -> None:
    cv.namedWindow("Image Display", cv.WINDOW_KEEPRATIO)
    cv.imshow(label, img)

    wait_time = 1000

    while cv.getWindowProperty(label, cv.WND_PROP_VISIBLE) >= 1:
        keyCode = cv.waitKey(wait_time)

        if (keyCode & 0xFF) == ord("q"):
            cv.destroyAllWindows()
            break


def plot_histogram(histogram: np.ndarray) -> None:
    grayscale_levels = np.arange(0, len(histogram))

    plt.figure(figsize=(8,6))
    plt.bar(
        x=grayscale_levels,
        height=histogram,
        color='gray'
    )
    plt.title(f"Image Histogram")
    plt.xlabel("Grayscale level")
    plt.ylabel("Pixel count")
    plt.show()


def plot_histogram_prob(histogram: np.ndarray, img: np.ndarray) -> None:
    grayscale_levels = np.arange(0, len(histogram))
    normalized_histogram = histogram / (img.shape[0] * img.shape[1])

    cumulative_prob = sampling.cumulative_probability(normalized_histogram)

    plt.figure(figsize=(18,5))
    ax1 = plt.subplot(121)
    ax1.bar(
        x=grayscale_levels,
        height=normalized_histogram,
        color='gray',
    )
    ax1.set_title('Probabilistic Histogram')
    ax2 = plt.subplot(122)
    ax2.plot(
        grayscale_levels,
        cumulative_prob,
        color='black',
    )
    ax2.set_title('Cumulative Probability')
    plt.show()


def plot_linear_function(coeficients: tuple, p1: tuple, p2: tuple) -> None:
    A, b = coeficients

    x = np.arange(*GRAYSCALE_DOMAIN)
    y = A*x + b

    plt.figure(figsize=(10,5))
    plt.plot(x, y, color='gray')
    plt.plot(p1[0], p1[1], 'bo')
    plt.plot(p2[0], p2[1], 'go')
    plt.xlim(GRAYSCALE_DOMAIN)
    plt.ylim(GRAYSCALE_DOMAIN)
    plt.grid()
    plt.show()
