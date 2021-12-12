import os, sys
# import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2 as cv
from numpy.lib.histograms import histogram    

import imgio
from core import intensity, filtering, kernels, sampling
from image_processor import ImageContext

DEFAULT_IMGPATH = os.path.join(os.getcwd(), "imgs")


if __name__ == '__main__':

    image_context = ImageContext().load_image('imgs/florida-noisy.png')
    image_context.to_grayscale()
    # image_context.apply_transform(intensity.normalize)
    img = image_context.image


    # img = np.random.randint(0, 255, size=16, dtype=np.uint8)
    # img = img.reshape((4, 4))
    # img = img / 255.0

    img_t = np.fft.fft2(img)
    
    img_texib = np.real(img_t)

    img_texib = np.fft.fftshift(img_texib)

    # Normalize the huge gap between frequencies
    img_texib = intensity.rescale(img_texib)

    # # (De-normalize) Convert to [0-255] scale
    img_texib = intensity.denormalize(img_texib)

    # # Apply histogram equalization
    img_texib_eq = sampling.equalize_histogram(img_texib)

    # # Normalize again
    img_texib_eq = intensity.normalize(img_texib_eq)

    # # Invert spectrum to have highest freqs as white
    img_texib_eq = intensity.negative(img_texib_eq)
