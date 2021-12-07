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
# from core.filtering import FILTER_IDENTITY

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

    # my_image = np.asarray(
    #     dtype=np.uint8,
    #     a=[[7, 6, 5, 5, 6, 7],
    #        [6, 4, 3, 3, 4, 6],
    #        [5, 3, 2, 2, 3, 5],
    #        [5, 3, 2, 2, 3, 5],
    #        [6, 4, 3, 3, 4, 6],
    #        [7, 6, 5, 5, 6, 7]]
    # )

    image_context = ImageContext().load_image('imgs/house.png')
    image_context.to_grayscale()
    # image_context.apply_transform(intensity.normalize)
    my_image = image_context.image

    imgio.display_image(my_image)
    sampling.histogram_normalized(my_image, plot=True)
    eq_my_image = sampling.equalize_histogram(my_image)
    sampling.histogram_normalized(eq_my_image, plot=True)
    imgio.display_image(eq_my_image)


if __name__ == '__main__':
    run_debug_mode()