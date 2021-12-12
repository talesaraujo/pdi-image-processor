from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from numpy.lib.npyio import load

from image_processor import ImageContext

import cv2 as cv
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {"message": "Hello World! It's working!!"}


@app.post("/image", status_code=202)
def send_image(image_file: UploadFile=File(...)):
    
    # with image_file.file as imgfile:
    #     io_buf = imgfile._file
    #     decoded_img = cv.imdecode(np.frombuffer(io_buf.getbuffer(), np.uint8), -1)

    context = ImageContext.load_image_from_buffer(image_file)
    context.to_grayscale()
    

    # img_gray = cv.cvtColor(decoded_img, cv.COLOR_BGR2GRAY)

    print(context.image)

    # cv.imwrite('image-gray-transformed.jpg', img_gray)

    return {
        "filename": image_file.filename
    }
