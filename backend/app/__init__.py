from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from image_processor import ImageContext

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

    context = ImageContext.load_image_from_buffer(image_file)
    context.to_grayscale()
    
    print(context.image)

    return {
        "filename": image_file.filename
    }
