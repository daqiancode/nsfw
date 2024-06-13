from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile
from app.conf import get_env_int
from fastapi.responses import Response
from transformers import AutoModelForImageClassification, ViTImageProcessor
import torch
from PIL import Image


app = FastAPI()

supported_image_formats = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'tiff']
def is_supported_image_format(filename: str):
    return filename.split('.')[-1] in supported_image_formats

model = AutoModelForImageClassification.from_pretrained("Falconsai/nsfw_image_detection")
processor = ViTImageProcessor.from_pretrained('Falconsai/nsfw_image_detection')

@app.post("/nsfw" , summary=f"Detect NSFW images. support {supported_image_formats}")
def create_upload_files(files: list[UploadFile] , response: Response):
    try:
        MaxUploadedFileCount = get_env_int("MAX_UPLOADED_FILE_COUNT", 100)
        if len(files) > MaxUploadedFileCount:
            response.status_code = 400
            return {"error": f"Number of files should be less than {MaxUploadedFileCount}"}
        MaxUploadedFileSize = get_env_int("MAX_UPLOADED_FILE_SIZE", 20) * 1024 * 1024
        if any(file.size > MaxUploadedFileSize for file in files):
            response.status_code = 400
            return {"error": f"File size should be less than {MaxUploadedFileSize} bytes"}
        ## filter empty files(size=0)
        if not all([is_supported_image_format(file.filename) for file in files]):
            response.status_code = 400
            return {"error": f"Only support image files with extensions {supported_image_formats}"}
        
        # Use a pipeline as a high-level helper
        # pipe = pipeline("image-classification", model="Falconsai/nsfw_image_detection")
        imgs = [Image.open(file.file) for file in files]
        exts = [file.filename.split('.')[-1].lower() for file in files]
        # extract first frame from gif
        imgs = [img.convert('RGB') if ext == 'gif' else img for img, ext in zip(imgs, exts)]
        # handle: Unsupported number of image dimensions: 2
        imgs = [img if len(img.size) == 3 else img.convert('RGB') for img in imgs]
        with torch.no_grad():
            inputs = processor(images=imgs, return_tensors="pt")
            outputs = model(**inputs)
            logits = outputs.logits

        predicted_label = logits.argmax(-1).tolist()
        return predicted_label

    finally:
        for file in files:
            file.file.close()


@app.post("/health")
def health():
    return {"status": "ok"}