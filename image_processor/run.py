import os
import sys; sys.path.insert(1, os.path.join(sys.path[0], '..'))
# import argparse
import numpy as np
import imgio
import pickle

from image_processor import ImageContext
from decompr.huffman import HuffmanStrategy
from decompr.lzw import LZWStrategy
from decompr import img_parser
from core import intensity, filtering, kernels, sampling
from typing import Any

BENCHIMAGE_PATH = 'imgs/benchmark.bmp'
# BENCHIMAGE_PATH = 'imgs/ladybird.bmp'


if __name__ == '__main__':

    # img_cxt = ImageContext().read_image(img_path=BENCHIMAGE_PATH)
    # imgio.display(img_cxt.image)
    # print(img_parser.bytes_to_integer(bvalue))

    # Num bits actually used by image data
    # 6819840

    LZWStrategy.compress_file(BENCHIMAGE_PATH)
    LZWStrategy.decompress_file(f"{BENCHIMAGE_PATH[:-4]}.lzw")


    # def int_to_bytes(x: int) -> bytes:
    #     return x.to_bytes((x.bit_length() + 7) // 8, 'big')
        
    # def int_from_bytes(xbytes: bytes) -> int:
    #     return int.from_bytes(xbytes, 'big')