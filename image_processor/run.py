import os
import sys; sys.path.insert(1, os.path.join(sys.path[0], '..'))
# import argparse
import numpy as np
import imgio
from image_processor import ImageContext
from decompr import huffman
from core import intensity, filtering, kernels, sampling
from typing import Any

# TODO: Create CLI (maybe?)

if __name__ == '__main__':

    icontext = ImageContext().read_image('imgs/benchmark.bmp')
    img = icontext.image
    img = img[:, :, 0]

    fqs = sampling.histogram(img)

    huffman.HuffmanCoding.encode(fqs)
    