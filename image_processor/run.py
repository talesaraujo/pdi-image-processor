import os
import sys; sys.path.insert(1, os.path.join(sys.path[0], '..'))
# import argparse
import numpy as np
import imgio

from image_processor import ImageContext
from decompr.huffman import HuffmanCoding
from core import intensity, filtering, kernels, sampling
from typing import Any
from loguru import logger

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

    icontext = ImageContext().read_image('imgs/benchmark.bmp')
    img = icontext.image
    img = img[:, :, 0]
    fqs = sampling.histogram(img)
    # fqs = np.array([5, 1, 6, 3])
    # fqs = np.array([7, 1, 6, 2, 5])
    fqs = np.array([10, 15, 12, 3, 4, 13, 1])

    max_value = np.max(fqs)
    max_index = fqs.tolist().index(max_value)

    min_value = np.min(fqs)
    min_index = fqs.tolist().index(min_value)

    huff_tree = HuffmanCoding.generate_tree(fqs)

    codes = HuffmanCoding.get_codes(huff_tree)

    logger.debug(f"Most frequent value: {max_index}")
    logger.debug(f"Least frequent value: {min_index}")
