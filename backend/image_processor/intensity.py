import os
import numpy as np
import cv2 as cv

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
