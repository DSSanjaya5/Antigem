from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import os
import base64
from uuid import uuid4

from middlewares.cache_middleware import CacheMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)   

ENDPOINT = "endpoint"
IMAGE_DIR = "processed_images"
os.makedirs(IMAGE_DIR, exist_ok=True)

@app.post(f"/{ENDPOINT}/{{filename}}")
async def process_image(filename: str, file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    
    # Call the Image processing function
    image = image.convert("L")

    filename = filename + "_" + ENDPOINT
    image_path = os.path.join(IMAGE_DIR, f"{filename}.jpg")
    image.save(image_path)

    # Encode the processed image to base64
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    # Return the base64 encoded image in a JSON response
    return {"filename": filename, "image_base64": encoded_image}

@app.get("/download-image/{filename}")
async def download_image(filename: str):
    image_path = os.path.join(IMAGE_DIR, f"{filename}.jpg")
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(image_path, media_type="image/jpeg", filename=f"{filename}.jpg")

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)