import io
import cv2 as cv

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from image_processor import ImageContext

app = FastAPI()

img_context = ImageContext()

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

    img_context.set_from_buffer(image_file)
    img_context.to_grayscale()
    
    print(img_context.image)

    return {
        "filename": image_file.filename
    }


@app.get("/image", status_code=200)
def get_image_context():

    res, img_jpg = img_context.as_buffer()
    return StreamingResponse(io.BytesIO(img_jpg.tobytes()), media_type="image/png")
