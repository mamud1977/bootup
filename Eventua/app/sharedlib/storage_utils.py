# storage_utils.py
import os
import re
from typing import Tuple
import aiofiles
import boto3
from fastapi import UploadFile, Depends

import asyncio 
from io import BytesIO
from urllib.parse import quote

from app.sharedlib.pydantic_utils import (
    EventStructure, 
    TokenData
)    

from app.sharedlib.util import (
    get_current_user
    )


# Decide storage backend
#STORAGE_TYPE = os.getenv("STORAGE_TYPE", "cloud")   # "local" or "cloud"
#STORAGE_TYPE = "local"
STORAGE_TYPE = "cloud"

# Local storage config
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "eventua_local_bucket")

# Cloud storage config
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET", "eventua_s3_bucket")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")




# Ensure local folder exists
if STORAGE_TYPE == "local":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Initialize S3 client only if needed
s3_client = None
if STORAGE_TYPE == "cloud":
    s3_client = boto3.client("s3", region_name=AWS_REGION)
    
# ---------- Helper functions ----------

def normalize_storage_key_for_url(storage_key: str) -> str:
    """Convert storage key to URL-safe format."""
    return quote(storage_key.replace("\\", "/"))


def safe_string(text: str) -> str:
    """Convert arbitrary text into filesystem-safe string (preserves extension)."""
    text = text.strip().lower()
    base, ext = os.path.splitext(text)
    base = re.sub(r"\s+", "_", base)
    base = re.sub(r"[^a-z0-9_]", "", base)
    ext = re.sub(r"[^a-z0-9.]", "", ext)
    return f"{base}{ext}"

def detect_content_type(filename: str) -> str:
    """Return MIME type based on file extension."""
    ext = os.path.splitext(filename)[1].lower()
    return {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".pdf": "application/pdf"
    }.get(ext, "application/octet-stream")

# ---------- File save logic (kept parameters intact) ----------
async def save_file(
    file: UploadFile,
    event_name: str,
    event_year: str,
    current_user: TokenData
) -> dict:
    
    try:
        print("save_file called")

        storagePath = os.path.join(
            current_user.username,
            str(event_year or "unknown_year"),
            safe_string(event_name)
        )
            
        storageKey = os.path.join(
            storagePath,
            safe_string(file.filename)
        )        

        print(storagePath)
        print(storageKey)
    

        if STORAGE_TYPE == "local":
            try:
               
                file_path = os.path.join(UPLOAD_FOLDER, storageKey) 
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                                 
                # Clear folder (only one file expected) 
                folder = os.path.dirname(file_path) 
                for old_file in os.listdir(folder): 
                    os.remove(os.path.join(folder, old_file))
                    
                # Save new file 
                async with aiofiles.open(file_path, "wb") as out_file: 
                    content = await file.read() 
                    await out_file.write(content) 
                file.file.seek(0)
                
                # Build JSON response 
                return { 
                    "storagePath": storagePath, 
                    "storageKey": storageKey, 
                    "file_name": file.filename, 
                    "file_ext": os.path.splitext(file.filename)[1].lower() if file.filename else None, 
                    "file_size": len(content), 
                    "file_content_type": file.content_type 
                }

            except Exception as e: 
                print("Local storage error:", e) 
                raise

        elif STORAGE_TYPE == "cloud":
            try:
                s3_client.head_bucket(Bucket=AWS_S3_BUCKET)
                
                # Delete old objects under the same prefix
                response = s3_client.list_objects_v2(Bucket=AWS_S3_BUCKET, Prefix=storagePath)
                for obj in response.get("Contents", []):
                    s3_client.delete_object(Bucket=AWS_S3_BUCKET, Key=obj["Key"])
            

                # Calculate file size 
                file.file.seek(0, os.SEEK_END) 
                size = file.file.tell() 
                file.file.seek(0)
                
                # Upload file
                s3_client.upload_fileobj(file.file, AWS_S3_BUCKET, storageKey)
                

                # Build JSON response 
                return { 
                    "storagePath": storagePath, 
                    "storageKey": storageKey, 
                    "file_name": file.filename, 
                    "file_ext": os.path.splitext(file.filename)[1].lower() if file.filename else None, 
                    "file_size": size, 
                    "file_content_type": file.content_type 
                }

            except Exception as e: 
                print("Cloud storage error:", e) 
                raise

        else: 
            raise ValueError(f"Unsupported STORAGE_TYPE: {STORAGE_TYPE}")

    except Exception as e:
        print("Unexpected error in save_file:", e) 
        raise


# ---------- Get file URL (kept parameter intact) ----------

def get_file_url(storageKey: str, content_type: str) -> str:
    print("get_file_url invoked")
    if not storageKey:
        return None

    if STORAGE_TYPE == "local":
        safe_key = normalize_storage_key_for_url(storageKey)
        file_url = f"/{UPLOAD_FOLDER}/{safe_key}"
        return file_url


    elif STORAGE_TYPE == "cloud":
        try:
            file_url = s3_client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": AWS_S3_BUCKET,
                    "Key": storageKey,  # always use original key
                    "ResponseContentDisposition": "inline",
                    "ResponseContentType": content_type
                },
                ExpiresIn=3600
            )
            return file_url

        except Exception as e:
            raise RuntimeError(f"Failed to generate presigned URL: {e}")

    else:
        raise ValueError(f"Unsupported STORAGE_TYPE: {STORAGE_TYPE}")


# ---------- Debug prints ----------
if __name__ == "__main__":
    print("STORAGE_TYPE:", STORAGE_TYPE)
    print("UPLOAD_FOLDER:", UPLOAD_FOLDER)
    print("AWS_S3_BUCKET:", AWS_S3_BUCKET)
    print("AWS_REGION:", AWS_REGION)

    
  

