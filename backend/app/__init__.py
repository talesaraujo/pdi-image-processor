from fastapi import FastAPI, File, UploadFile
# from image_processor import input

import cv2 as cv
import numpy as np

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World! It's working!!"}


@app.post("/image", status_code=202)
def send_image(image_file: UploadFile=File(...)):
    
    with image_file.file as imgfile:
        io_buf = imgfile._file
        decoded_img = cv.imdecode(np.frombuffer(io_buf.getbuffer(), np.uint8), -1)

    img_gray = cv.cvtColor(decoded_img, cv.COLOR_BGR2GRAY)

    print(img_gray)

    # cv.imwrite('image-gray-transformed.jpg', img_gray)

    return {
        "filename": image_file.filename
    }
