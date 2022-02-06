import os
import sys; sys.path.insert(1, os.path.join(sys.path[0], '..'))
# import argparse
import numpy as np
import imgio

from image_processor import ImageContext
from decompr.huffman import HuffmanCoding
from decompr import img_parser
from core import intensity, filtering, kernels, sampling
from typing import Any
from loguru import logger

BENCHIMAGE_PATH = 'imgs/benchmark.bmp'

logger.remove()
logger.add(
    sys.stderr,
    backtrace=True,
    diagnose=True,
    format="<green>{level}</green> | <level>{message}</level>",
    colorize=True,
    level="DEBUG"
)

# TODO: Create CLI (maybe?)

if __name__ == '__main__':

    # img_cxt = ImageContext().read_image(img_path=BENCHIMAGE_PATH)
    # imgio.display(img_cxt.image)
    # print(img_parser.bytes_to_integer(bvalue))

    pixels_info = img_parser.get_pixels_hexlist(BENCHIMAGE_PATH)
    pixels_info = img_parser.convert_to_decimal(pixels_info)

    for value in pixels_info[:10]:
        print(value)

