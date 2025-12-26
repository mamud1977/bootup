from fastapi import (
    APIRouter, 
    status, 
    HTTPException, 
    Depends, 
    Request, 
    Form,
    Query
)


import logging
 

from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

import sys
import json
from fastapi.responses import HTMLResponse, JSONResponse

from fastapi.templating import Jinja2Templates

from database.connection import get_connection
from sharedlib.util import get_jwt, get_current_user
from sharedlib import pydantic

from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

templates = Jinja2Templates(directory="templates")
# Load profiles from JSON file

import os
# import easyocr
# import magic 
  
router = APIRouter()

# @router.get("/test/easyocr", tags=['Test'])
# async def get_ocr_file(request: Request):
#     return templates.TemplateResponse( 
#         "test/easyocr.jinja",
#         {"request": request}
#     )

# @router.post("/test/easyocr", tags=['Test'])
# def process_ocr_file(request: Request):
#     api_name = "test/easyocr.jinja"
#     logging.info(f"I am invoked: {api_name}")

#     try:
        
#         error_message = None

#         DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
#         print(DATA_DIR)
        
#         files = os.listdir(DATA_DIR)
#         # Iterate through each file
#         file_list = []
#         # Iterate through each file
#         for filename in files:
#             file_path = os.path.join(DATA_DIR, filename)
#             if os.path.isfile(file_path):
#                 print(f"Found file: {filename} (full path: {file_path})")

#                 with open(file_path, "rb") as f:
#                     contents = f.read()

#                 mime_type = magic.from_buffer(contents, mime=True)
#                 file_info = {
#                     "filename": filename,
#                     "path": file_path,
#                     "extension": filename.split(".")[-1].lower(),
#                     "mime_type": mime_type
#                 }
#                 file_list.append(file_info)
#             else:
#                 print(f"Skipping non-file entry: {filename}")

    
#         reader = easyocr.Reader(['en', 'bn'])  # English + Bengali
#         result = reader.readtext('/mnt/c/MyWork/gitlocal/bootup/FastApi/data/1.jpeg')
#         print(result)


#         for row in file_list:
#             print(row)

#         reader = easyocr.Reader(['bn', 'en']) 
          
#         filename = "/mnt/c/MyWork/gitlocal/bootup/FastApi/data/1.jpeg"
#         results = reader.readtext(filename)
#         for bbox, text, confidence in results:
#             print(f"Detected text: {text} (confidence: {confidence:.2f})")


#     except Exception as e:
#         error_message = str(e)
               
#     return templates.TemplateResponse(
#         "test/easyocr.jinja",
#         {
#             "request": request, 
#             "response": file_list, 
#             "ocr_data": result,
#             "error_message": error_message
#         }
#     )


@router.get("/test/pramukhime", tags=['Test'])
def get_event(request: Request, eventname: Optional[str] = Query(None)):
    
    api_name = "test/pramukhime.jinja"
    logging.info("I am invoked: {api_name}")

    event_structure = None
    error_message = None

    
    return templates.TemplateResponse(
        "test/pramukhime.jinja",
        {
            "request": request, 
            "eventname": eventname, 
            "event_structure": event_structure,
            "error_message": error_message
        }
    )










