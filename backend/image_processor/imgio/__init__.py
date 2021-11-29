import numpy as np
import cv2 as cv

def display_image(img: np.ndarray, label: str="Image") -> None:
    # img = cv.resize(img, (3, 10))
    cv.imshow(label, img)
    cv.waitKey(0)
    cv.destroyAllWindows()
