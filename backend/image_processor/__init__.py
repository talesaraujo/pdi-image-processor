import os, sys
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2 as cv
from numpy.lib.histograms import histogram    

import imgio
from core import intensity, filtering, kernels, sampling
from typing import Any

DEFAULT_IMGPATH = os.path.join(os.getcwd(), "imgs")

class ImageContext:

    def __init__(self, image: Any=None) -> None:
        self.image = image
        self.prev_state = None

    @classmethod
    def load_image(cls, img_path) -> None:
        if not os.path.isfile(img_path):
            raise FileNotFoundError("No such file.")
        return cls(cv.imread(img_path, cv.IMREAD_COLOR))
    

    def to_grayscale(self) -> None:
        self.prev_state = self.image
        self.image = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)


    def undo(self) -> None:
        if self.prev_state is None:
            return None
        self.image = self.prev_state
    
    def apply_transform(self, transform_func) -> np.ndarray:
        self.prev_state = self.image
        self.image = transform_func(self.image)
        return self.image


def run_debug_mode():

    image_context = ImageContext().load_image('imgs/astronaut.png')
    image_context.to_grayscale()
    # image_context.apply_transform(intensity.normalize)
    my_image = image_context.image

    imgio.display_image(my_image)
    my_image_hist = sampling.histogram(img=my_image)
    imgio.plot_histogram_prob(my_image_hist, my_image)

    my_image_equalized = sampling.equalize_histogram(my_image)
    imgio.display_image(my_image_equalized)
    my_image_equalized_hist = sampling.histogram(img=my_image_equalized)
    imgio.plot_histogram_prob(my_image_equalized_hist, my_image_equalized)


if __name__ == '__main__':
    run_debug_mode()
