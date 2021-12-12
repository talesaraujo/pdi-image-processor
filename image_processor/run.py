import os
# import argparse
import numpy as np
import imgio
from core import intensity, filtering, kernels, sampling
from typing import Any

# TODO: Create CLI (maybe?)

if __name__ == '__main__':

    # image_context = ImageContext().load_image('imgs/lena_32.png')
    # image_context.to_grayscale()
    # # image_context.apply_transform(intensity.normalize)
    # img = image_context.image

    img = np.random.randint(0, 255, size=16, dtype=np.uint8)
    img = img.reshape((4, 4))
    # img = img / 255.0

    print("Image")
    print(img)
    print("")

    F_t = filtering.dft2(img)
    f_t = filtering.idft2(F_t)

    print("Image obtained from intensity.idft2")
    print(np.real(f_t))
    print("")

    F_np = np.fft.fft2(img)
    f_np = np.fft.ifft2(F_np)
    
    print("Image obtained from np.ifft2")
    print(np.real(f_np))
    print("")

    print(np.isclose(F_np, F_t))
    print(np.isclose(f_np, f_t))
