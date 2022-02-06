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

    # Num bits actually used by image data
    # 6819840

    pixels_binaries = img_parser.get_pixels_binlist(BENCHIMAGE_PATH)

    print(len(pixels_binaries))

    for pixel in pixels_binaries[:10]:
        print(pixel)
    
    print(len(pixels_binaries[0][1]))
