import os
import sys; sys.path.insert(1, os.path.join(sys.path[0], '..'))
# import argparse
import numpy as np
import imgio
from image_processor import ImageContext
from core import intensity, filtering, kernels, sampling
from typing import Any

# TODO: Create CLI (maybe?)

if __name__ == '__main__':

    # Applying Low Pass Filter and etc with Fourier Transform
    icontext = ImageContext().read_image('imgs/dunes.png')
    # icontext = ImageContext().read_image('imgs/lena_original.png')
    icontext.to_grayscale()
    icontext.normalize()

    # Display original image
    imgio.display(icontext.image)

    # Computing the Fourier Transform of the Image
    img_t = np.fft.fft2(icontext.image)

    # Apply rescaling (to avoid negative values)
    # img_t = intensity.rescale(img_t)

    # Shifting frequencies to origin
    img_t = np.fft.fftshift(img_t)

    # Display Fourier Transform (absolute value)
    img_t_d = np.abs(img_t)

    # Cropping to remove extreme values
    img_t_d[img_t_d  > 2000] = 2000

    # Apply rescaling/normalization (to avoid negative values)
    img_t_d = intensity.rescale(img_t_d)    

    # Display the VISUALIZATION of the Fourier Transform
    imgio.display(img_t_d)

    print(img_t.shape, img_t_d.shape)

    # Display selected filter
    # radius = 40
    # c_filter = filtering.get_circular_filter(radius, gaussian=True)
    # c_filter = intensity.normalize(c_filter)
    # imgio.display(c_filter)
    # print(c_filter.shape)

    # Reshape filter to fit the transformed image size
    # complete_filter = np.zeros(img_t.shape) # or ones...
    complete_filter = filtering.gen_image_filter(
        img_source=img_t,
        radius=30,
        gaussian=True
    )

    # Compute halves to easy calculation
    # half_shape = tuple(np.array(img_t.shape) / 2)
    # half_shape = tuple(int(np.floor(value)) for value in half_shape)

    # if radius % 2 == 0:
    #     radius += 1

    # complete_filter[
    #     half_shape[0]-radius:half_shape[0]+radius+1,
    #     half_shape[1]-radius:half_shape[1]+radius+1
    # ] = c_filter

    assert complete_filter.shape == img_t.shape

    # complete_filter_inv = intensity.negative(complete_filter)
    # complete_filter_inv = intensity.normalize(complete_filter_inv)

    imgio.display(intensity.rescale(complete_filter))

    # Applying filter over fft transformed image
    img_t_proc = np.multiply(img_t, complete_filter)

    # Display Processed Transformed Image (absolute value)
    img_t_proc_d = np.abs(img_t_proc)

    # Cropping to remove extreme values
    img_t_proc_d[img_t_proc_d > 1000] = 1000

    # Rescale 
    img_t_d = intensity.normalize(img_t_d)

    # Display Processed Transformed Image
    # imgio.display(img_t_proc_d)

    # Apply Inverse Fourier Transform
    img_t_proc = np.fft.ifftshift(img_t_proc)
    img_proc = np.fft.ifft2(img_t_proc)

    # See the results I guess?
    img_proc_d = np.real(img_proc)

    img_proc_d = intensity.rescale(img_proc_d)

    imgio.display(img_proc_d)




    # imgio.display(disk_filter * 
    # # image_context.apply_transform(intensity.normalize)
    # img = image_context.image

    # img = np.random.randint(0, 255, size=16, dtype=np.uint8)
    # img = img.reshape((4, 4))
    # # img = img / 255.0

    # print("Image")
    # print(img)
    # print("")

    # F_t = filtering.dft2(img)
    # f_t = filtering.idft2(F_t)

    # print("Image obtained from intensity.idft2")
    # print(np.real(f_t))
    # print("")

    # F_np = np.fft.fft2(img)
    # f_np = np.fft.ifft2(F_np)
    
    # print("Image obtained from np.ifft2")
    # print(np.real(f_np))
    # print("")

    # print(np.isclose(F_np, F_t))
    # print(np.isclose(f_np, f_t))
