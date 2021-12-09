import os, sys
# import argparse
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
        self.prev_state = image

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
        """TODO: Refactor in order to support function inner arguments"""
        self.prev_state = self.image
        self.image = transform_func(self.image)
        return self.image
    
    def apply_rescaling(self) -> None:
        """TODO: Check for the possibility of having an image already within 
        the desired range."""
        self.image += np.abs(np.min(self.image))
        self.image /= np.max(self.image) 


if __name__ == '__main__':

    image_context = ImageContext().load_image('imgs/ufc2.jpg')
    image_context.to_grayscale()
    # image_context.apply_transform(intensity.normalize)
    img = image_context.image

    # imgio.display_image(my_image)
    # print(my_image)

    # my_image_t = filtering.convolve2D(image_context.image, kernels.LAPLACIAN)

    # imgio.display_image(my_image_transformed)

    # scalar-sum the lowest value (absolute) out of the matrix 
    # scalar-divide the matrix by the biggest value out of the matrix
