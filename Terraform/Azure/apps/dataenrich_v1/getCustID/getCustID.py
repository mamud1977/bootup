import azure.functions as func
from azure.storage.blob import BlobServiceClient
import datetime
import json
import logging
import os
#import polars as pl
import pandas as pd

from helper import dump_json
from io import BytesIO
import gc



def getCustNumber(req: func.HttpRequest) -> func.HttpResponse:

    try:

        logging.info("Start processing to get customers")

        try:
            req_body = req.get_json() # Try to parse the incoming request's body as JSON
            logging.info("Received JSON body:\n%s", json.dumps(req_body, indent=2))
        
        except ValueError:
            # Return a bad request response (400) if JSON parsing fails
            return func.HttpResponse(
                "Invalid JSON input",
                status_code=500
            )

        try:
            json_input, document_type = dump_json(req_body)
            logging.info(f"DOCUMENT TYPE: {document_type}")
            logging.info(f"json_input: {json.dumps(json_input)}")

        except (json.JSONDecodeError, KeyError) as e:
            logging.error(f"Invalid input JSON: {str(e)}")
            return func.HttpResponse(
                body=json.dumps({"error": "Invalid input format"}),
                status_code=500,
                mimetype="application/json"
            )
        

        # Get connection string from environment
        try:
            conn_str = os.getenv("AzureWebJobsStorage")
            container_name = "parquet-files"
            blob_service_client = BlobServiceClient.from_connection_string(conn_str)
            container_client = blob_service_client.get_container_client(container_name)

            # Example: list blobs
            blob_list = [blob.name for blob in container_client.list_blobs()]
            logging.info(f"blob_list: {blob_list}")

            
            # Get a blob client to interact with a specific file (blob) within the container
            blob_path = "mtcars.parquet"
            blob_client = container_client.get_blob_client(blob_path)

            # Download the blob's content (file) as a stream
            stream_downloader = blob_client.download_blob()
            logging.info("Blob downloaded successfully")

            # Convert the downloaded blob content into an in-memory byte stream
            blob_data = BytesIO(stream_downloader.readall())
            size_bytes = blob_data.getbuffer().nbytes
            
            logging.info(f"Blob content loaded into memory as a byte stream, and size = {size_bytes}")

        except Exception as e:
            logging.error(f"Error: {e}")
            return func.HttpResponse("Failed to connect to container", status_code=500)


        try:

            #temp_df = pl.read_parquet(blob_data) 
            temp_df = pd.read_parquet(blob_data) 

            del blob_data
            gc.collect()  # Explicitly trigger garbage collection to free memory

            logging.info(f"temp_df dimension = {temp_df.shape}")
            for index, row in temp_df.iterrows():
                logging.info(f"Row {index}: {row.to_dict()}")

        except Exception as e:
            logging.error(f"Error: {e}")
            return func.HttpResponse(f"Parquet loading failed: {str(e)}", status_code=500)


        return func.HttpResponse(
            "This HTTP triggered function executed successfully",
            status_code=200
            )
    
    except Exception as e:
        return func.HttpResponse(
        f"Exception: {e}",
        status_code=500
        )
