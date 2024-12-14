from PIL import Image
import pytesseract
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor

# Set up the Tesseract executable path (if on Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# def extract_text_from_image(image_bytes: bytes,keywords) -> str:
#     try:
#         # Open the image from the bytes data
#         image = Image.open(BytesIO(image_bytes))
#         print(keywords)
#         # Use pytesseract to do OCR on the image
#         extracted_text = pytesseract.image_to_string(image)
        
#         return extracted_text
#     except Exception as e:
#         return f"Error: {str(e)}"


def extract_text_from_image(image_bytes: bytes) -> str:
    try:
        # Open the image from the bytes data
        image = Image.open(BytesIO(image_bytes))
        # Use pytesseract to do OCR on the image
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text
    except Exception as e:
        return f"Error: {str(e)}"

def search_keywords_in_chunks(text: str, keywords: list) -> list:
    """
    Splits the text into chunks of 10 lines and searches for keywords in each chunk.
    Returns a list of results where keywords are found, including the full line containing the keyword.
    """
    lines = text.splitlines()
    chunks = ["\n".join(lines[i:i + 10]) for i in range(0, len(lines), 10)]
    results = []

    for chunk in chunks:
        for line in chunk.splitlines():
            for keyword in keywords:
                if keyword in line:
                    results.append({"line": line, "keyword": keyword})
                    break  # Break to avoid duplicate results for the same line

    return results

def process_image(image_bytes: bytes, keywords: list) -> dict:
    """Processes a single image: extracts text and searches for keywords."""
    text = extract_text_from_image(image_bytes)
    if text.startswith("Error:"):
        return {"error": text}
    results = search_keywords_in_chunks(text, keywords)
    return {"results": results}

def process_images_parallel(image_data_list: list, keywords: str) -> dict:
    """
    Processes multiple images in parallel.

    Args:
        image_data_list: List of image byte data.
        keywords: Comma-separated string of keywords to search for.

    Returns:
        Dictionary containing the results for each image.
    """
    keywords_list = keywords.split(",")
    results = {}

    with ThreadPoolExecutor() as executor:
        futures = {
            idx: executor.submit(process_image, image_bytes, keywords_list)
            for idx, image_bytes in enumerate(image_data_list)
        }

        for idx, future in futures.items():
            results[f"Image_{idx + 1}"] = future.result()

    return results

