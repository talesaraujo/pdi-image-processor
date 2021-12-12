import numpy as np
import cv2 as cv
import os
from typing import Any

class ImageContext:

    def __init__(self, image: Any=None) -> None:
        self.image = image
        self.prev_state = np.array(self.image, copy=True)

    @classmethod
    def load_image(cls, img_path) -> None:
        if not os.path.isfile(img_path):
            raise FileNotFoundError("No such file.")
        return cls(cv.imread(img_path, cv.IMREAD_COLOR))

    @classmethod
    def load_image_from_buffer(cls, img_file):
        with img_file.file as imgfile:
            io_buf = imgfile._file
            decoded_img = cv.imdecode(np.frombuffer(io_buf.getbuffer(), np.uint8), -1)
        return cls(decoded_img)

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
