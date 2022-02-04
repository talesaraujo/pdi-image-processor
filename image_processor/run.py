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

    # # img_parser.parse_imgfile(BENCHIMAGE_PATH)
    # filetype, filesize, reserved_4 = img_parser.parse_imgfile(BENCHIMAGE_PATH)
    # filetype, filesize, reserved_4 = b''.join(filetype), b''.join(filesize), b''.join(reserved_4)

    # print(filetype.hex())
    # print(filesize.hex())


    # # print(filetype.decode('ASCII'))
    # print(int.from_bytes(filesize, byteorder="little", signed=False))

    # print(int.from_bytes(reserved_4, byteorder="little", signed=False))

    # bvalue = img_parser.read_file_slice(
    #     img_fpath=BENCHIMAGE_PATH,
    #     start_byte=2,
    #     end_byte=6
    # )

    # print(img_parser.bytes_to_integer(bvalue))
    img_parser.parse_imgfile(BENCHIMAGE_PATH)

