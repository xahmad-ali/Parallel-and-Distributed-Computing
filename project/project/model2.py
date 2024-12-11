# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import JSONResponse
# from PIL import Image
# import pytesseract
# import os
# from io import BytesIO

# app = FastAPI()

# # Set up the Tesseract executable path (if on Windows)
# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# from fastapi.middleware.cors import CORSMiddleware

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Or specify the frontend URL, e.g., ["http://localhost:3000"]
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )



# def extract_text_from_image(image_bytes: bytes) -> str:
#     try:
#         # Open the image from the bytes data
#         image = Image.open(BytesIO(image_bytes))
        
#         # Use pytesseract to do OCR on the image
#         extracted_text = pytesseract.image_to_string(image)
        
#         return extracted_text
#     except Exception as e:
#         return f"Error: {str(e)}"

# @app.post("/extract-text")
# async def extract_text(file: UploadFile = File(...)):
#     if not file:
#         return JSONResponse(content={"error": "No file uploaded"}, status_code=400)
#     if file.content_type not in ["image/jpeg", "image/png"]:
#         return JSONResponse(content={"error": "Unsupported file type"}, status_code=400)
    
#     image_bytes = await file.read()
#     extracted_text = extract_text_from_image(image_bytes)
#     return JSONResponse(content={"extracted_text": extracted_text})

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import pytesseract
from io import BytesIO
from typing import List

app = FastAPI()

# Set up the Tesseract executable path (if on Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify the frontend URL, e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_from_image(image_bytes: bytes) -> str:
    try:
        # Open the image from the bytes data
        image = Image.open(BytesIO(image_bytes))
        
        # Use pytesseract to do OCR on the image
        extracted_text = pytesseract.image_to_string(image)
        
        return extracted_text
    except Exception as e:
        return f"Error: {str(e)}"

@app.post("/extract-text")
async def extract_text(files: List[UploadFile] = File(...)):
    if not files:
        return JSONResponse(content={"error": "No files uploaded"}, status_code=400)
    
    results = {}
    for i, file in enumerate(files):
        if file.content_type not in ["image/jpeg", "image/png"]:
            results[file.filename] = "Unsupported file type"
            continue

        image_bytes = await file.read()
        extracted_text = extract_text_from_image(image_bytes)
        results[file.filename] = extracted_text

    return JSONResponse(content={"results": results})


