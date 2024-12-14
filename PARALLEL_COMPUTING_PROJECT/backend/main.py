from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from typing import List
import uuid 
import os


from image_model import process_images_parallel
from excell_model import process_files_dynamically

app = FastAPI()



from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify the frontend URL, e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.post("/extract-text")
# async def extract_text(
#     files: List[UploadFile] = File(...),
#     keywords: str = Form(...),
#     ):
#     if not files:
#         return JSONResponse(content={"error": "No files uploaded"}, status_code=400)
#     print(keywords)
    
#     results = {}
#     for i, file in enumerate(files):
#         if file.content_type not in ["image/jpeg", "image/png"]:
#             results[file.filename] = "Unsupported file type"
#             continue

#         image_bytes = await file.read()
#         extracted_text = process_images_parallel(image_bytes,keywords)
#         results[file.filename] = extracted_text

#     return JSONResponse(content={"results": results})

@app.post("/extract-text")
async def extract_text(
    files: List[UploadFile] = File(...),
    keywords: str = Form(...),
):
    if not files:
        return JSONResponse(content={"error": "No files uploaded"}, status_code=400)

    results = {}
    for i, file in enumerate(files):
        if file.content_type not in ["image/jpeg", "image/png"]:
            results[file.filename] = "Unsupported file type"
            continue

        image_bytes = await file.read()
        result = process_images_parallel([image_bytes], keywords)
        results[file.filename] = result.get("Image_1", {})
        print(result)

    return JSONResponse(content={"results": results})




import pandas as pd
from starlette.responses import JSONResponse
from io import BytesIO
from starlette.responses import StreamingResponse

@app.post("/search")
async def search_files(
    files: List[UploadFile] = File(...),
    pattern: str = Form(...),
):
    try:
        print("working 1")
        keywords = [keyword.strip().lower() for keyword in pattern.split(',') if keyword.strip()]
        
        print("Keywords:", keywords)
        results = []
        print(pattern)

        temp_dir = "\\backend\\tmp"
        os.makedirs(temp_dir, exist_ok=True)

        # Save and process uploaded files
        file_paths = []
        for file in files:
            # Generate a unique path for each file in the temp directory
            temp_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")
            with open(temp_path, "wb") as f:
                f.write(await file.read())
            
            file_paths.append(temp_path)  # Add to list of file paths

        # Process files for keyword matching
        print("working 2")
        file_results = process_files_dynamically(file_paths, keywords)
        
        # Since results are already dictionaries, we can use them directly
        serializable_results = file_results

        # Create an XLSX file from the results
        if file_results:
            result_df = pd.DataFrame(file_results)
        else:
            result_df = pd.DataFrame(columns=["No Results"])  # Create an empty dataframe if no results found

        output = BytesIO()
        result_df.to_excel(output, index=False)
        output.seek(0)

        # Clean up temp files
        for temp_path in file_paths:
            os.remove(temp_path)

        # Send the XLSX file as a StreamingResponse
        headers = {
            "Content-Disposition": f'attachment; filename="search_results.xlsx"'
        }
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers=headers
        )

    except Exception as e:
        print(f"Error in search_files: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(content={"error": str(e)}, status_code=500)

# @app.post("/search")
# async def search_files(
#     files: List[UploadFile] = File(...),
#     pattern: str = Form(...),
# ):
#     try:
#         print("working 1")
#         keywords = [keyword.strip().lower() for keyword in pattern.split(',') if keyword.strip()]
        
#         print("Keywords:", keywords)
#         results = []
#         print(pattern)

#         temp_dir = "\\backend\\tmp"
#         os.makedirs(temp_dir, exist_ok=True)

#         # Save and process uploaded files
#         file_paths = []
#         for file in files:
#             # Generate a unique path for each file in the temp directory
#             temp_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")
#             with open(temp_path, "wb") as f:
#                 f.write(await file.read())
            
#             file_paths.append(temp_path)  # Add to list of file paths

#         # Process files for keyword matching
#         print("working 2")
#         file_results = process_files_dynamically(file_paths, keywords)
        
#         # Since results are already dictionaries, we can use them directly
#         serializable_results = file_results

#         # Create an XLSX file from the results
#         if file_results:
#             result_df = pd.DataFrame(file_results)
#         else:
#             result_df = pd.DataFrame(columns=["No Results"])  # Create an empty dataframe if no results found

#         output = BytesIO()
#         result_df.to_excel(output, index=False)
#         output.seek(0)

#         # Clean up temp files
#         for temp_path in file_paths:
#             os.remove(temp_path)

#         # Send both JSON response and the XLSX file
#         headers = {
#             "Content-Disposition": f'attachment; filename="search_results.xlsx"'
#         }
#         return FileResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)

#     except Exception as e:
#         print(f"Error in search_files: {e}")
#         import traceback
#         traceback.print_exc()
#         return JSONResponse(content={"error": str(e)}, status_code=500)
