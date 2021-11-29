import os, sys
import argparse
import numpy as np
import cv2 as cv    

import imgio
from core import intensity, filtering
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



def run(folder_path):

    image_context = ImageContext().load_image(folder_path)
    # image_context.load_image(folder_path)
    image_context.to_grayscale()
    image_context.apply_transform(intensity.normalize)
    
    imgio.display_image(image_context.image, label="Original Image")
    imgio.display_image(image_context.apply_transform(intensity.negative), label="Image inverted")
    
    # img = intensity.normalize(img)

    # imgio.display_image(img, label="UFC Original")
    # imgio.display_image(intensity.negative(img), label="UFC Inverted")


def run_debug_mode():

    # my_image = np.ndarray(shape=(6,6), dtype=int,)
    my_image = np.asarray(
        dtype=np.uint8,
        a=[[7, 6, 5, 5, 6, 7],
           [6, 4, 3, 3, 4, 6],
           [5, 3, 2, 2, 3, 5],
           [5, 3, 2, 2, 3, 5],
           [6, 4, 3, 3, 4, 6],
           [7, 6, 5, 5, 6, 7]]
    )

    my_filter = np.asarray(
        dtype=np.int8,
        a=[[ 0, -1,  0],
           [-1,  5, -1],
           [ 0, -1,  0]]
    )

    # ufc_image = cv.imread('imgs/ufc.jpg', cv.IMREAD_GRAYSCALE)
    
    # print(my_image)
    # print("")
    print(my_image)
    print("")
    print(filtering.convolve2D(img=my_image, filter=my_filter))

    # imgio.display_image(my_image)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input',
        metavar="",
        help="The folder directory in which the image is located on"
    )
    parser.add_argument(
        '-d', '--debug',
        action="store_true",
        help="Help with debugging option."
    )

    args = parser.parse_args()

    # If no argument is provided
    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    if args.input:
        run(args.input)

    if args.debug:
        run_debug_mode()
