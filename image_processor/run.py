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

BENCHIMAGE_PATH = 'imgs/benchmark.bmp'


# TODO: Create CLI (maybe?)

if __name__ == '__main__':

    # img_cxt = ImageContext().read_image(img_path=BENCHIMAGE_PATH)
    # imgio.display(img_cxt.image)
    # print(img_parser.bytes_to_integer(bvalue))

    # Num bits actually used by image data
    # 6819840

    pixels_dec = img_parser.get_pixels_declist(BENCHIMAGE_PATH)

    blue_channel, green_channel, red_channel = img_parser.parse_channels(pixels_dec)

    HuffmanCoding.encode(
        (blue_channel, green_channel, red_channel)
    )
