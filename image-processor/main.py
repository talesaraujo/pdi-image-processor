import os
import numpy as np
import cv2 as cv

DEFAULT_IMGPATH = os.path.join(os.getcwd(), "imgs")
print(os.getcwd())
print(DEFAULT_IMGPATH)


def display_image(img: np.ndarray, label: str="Image") -> None:
    cv.imshow(label, img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def normalize(img: np.ndarray) -> np.ndarray:
    return img / 255.0

def set_brightness(img: np.ndarray, factor: int) -> np.ndarray:
    return factor * img

def negative(img: np.ndarray) -> np.ndarray:
    return 1 - img

def log_transform(img: np.ndarray, c: int) -> np.ndarray:
    return c * np.log(1 + img)

def gamma_transform(img: np.ndarray, c: int, gamma: float) -> np.ndarray:
    return c * (img ** gamma)


if __name__ == '__main__':

    ufc_img = os.path.join(DEFAULT_IMGPATH, 'ufc.jpg')
    img = cv.imread(ufc_img, cv.IMREAD_GRAYSCALE)

    img = normalize(img)

    display_image(img, label="UFC Original")
    display_image(negative(img), label="UFC Inverted")
