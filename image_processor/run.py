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
        self.prev_state = np.array(self.image, copy=True)

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

    # image_context = ImageContext().load_image('imgs/lena_32.png')
    # image_context.to_grayscale()
    # # image_context.apply_transform(intensity.normalize)
    # img = image_context.image


    img = np.random.randint(0, 255, size=16, dtype=np.uint8)
    img = img.reshape((4, 4))
    # img = img / 255.0

    print("Image")
    print(img)
    print("")

    F_t = filtering.dft2(img)
    f_t = filtering.idft2(F_t)

    print("Image obtained from intensity.idft2")
    print(np.real(f_t))
    print("")

    F_np = np.fft.fft2(img)
    f_np = np.fft.ifft2(F_np)
    
    print("Image obtained from np.ifft2")
    print(np.real(f_np))
    print("")

    print(np.isclose(F_np, F_t))
    print(np.isclose(f_np, f_t))

