import os
import numpy as np
import cv2 as cv

from typing import Any
from image_processor.core import intensity


class ImageContext:

    def __init__(self, image: Any=None) -> None:
        self.image = image
        self.prev_state = np.array(self.image, copy=True)


    @classmethod
    def read_image(cls, img_path) -> None:
        if not os.path.isfile(img_path):
            raise FileNotFoundError("No such file.")
        return cls(cv.imread(img_path, cv.IMREAD_COLOR))


    def load_image(self, img_path) -> None:
        if not os.path.isfile(img_path):
            raise FileNotFoundError("No such file.")

        img = cv.imread(img_path, cv.IMREAD_COLOR)
        self.image = img
        self.prev_state = img


    def to_grayscale(self) -> None:
        self.image = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)


    def undo(self) -> None:
        if self.prev_state is None:
            return None
        self.image = self.prev_state
    

    def normalize(self) -> None:
        self.image = intensity.normalize(self.image)
        self.prev_state = intensity.normalize(self.prev_state)


    def denormalize(self) -> None:
        self.image = intensity.denormalize(self.image)
        self.prev_state = intensity.denormalize(self.prev_state)


    def apply_transform(self, transform_func, *args) -> np.ndarray:
        """TODO: Refactor in order to support function inner arguments"""
        self.prev_state = np.array(self.image, copy=True)
        self.image = transform_func(self.image, *args)
        return self.image


    def apply_rescaling(self) -> None:
        """TODO: Check for the possibility of having an image already within 
        the desired range."""
        self.image += np.abs(np.min(self.image))
        self.image /= np.max(self.image)
