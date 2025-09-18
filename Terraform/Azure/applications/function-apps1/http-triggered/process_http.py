import logging
import azure.functions as func
from rapidfuzz import fuzz, process
import pandas as pd
from azure.storage.blob import BlobServiceClient
import os
import io



def main(req: func.HttpRequest) -> func.HttpResponse:
    
    try:
        # Blob details
        container_name = "parquet-files"
        blob_name = "gold_vs_bitcoin.parquet"

        # Connect to Blob Storage
        conn_str = os.environ["AzureWebJobsStorage"]
        blob_service_client = BlobServiceClient.from_connection_string(conn_str)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        # Download blob content
        stream = blob_client.download_blob()
        parquet_bytes = stream.readall()

        # Read Parquet into DataFrame
        df = pd.read_parquet(io.BytesIO(parquet_bytes))

        # # Log and return summary
        # logging.info(f"Read {len(df)} rows from {blob_name}")
        
        # input_po_num = req.params.get("po_number")

        # choices = ["PO 12345", "POx 83n333", "PO 383838302"]

        # #Find top 3 matches
        # matches = process.extract(input_po_num, choices, limit=3)
        # print("Top matches:")
        # logging.info(f"Top matches:")
        # for match in matches:
        #     m = (input_po_num, match)
        #     print(match)
        #     logging.info(f"match:{m}")

        return func.HttpResponse(f"Parquet file '{blob_name}' has {len(df)} rows and {len(df.columns)} columns.", status_code=200)
    
    except Exception as e:
        return func.HttpResponse(f"Exception: {e}", status_code=500) 



