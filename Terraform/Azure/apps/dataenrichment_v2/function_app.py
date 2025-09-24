import azure.functions as func
from azure.storage.blob import BlobServiceClient
import datetime
import json
import logging
import os

from helper import dump_json

#app = func.FunctionApp()
app = func.Blueprint(http_auth_level = func.AuthLevel.FUNCTION)

#@app.function_name(name="getCustNumber")
app.route(route="getCustNumber",methods=['post'])
#@app.function_name(name="getCustNumber")
#@app.route(route="getCustNumber", auth_level=func.AuthLevel.FUNCTION)
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

            

        except Exception as e:
            logging.error(f"Error: {e}")
            return func.HttpResponse("Failed to connect to container", status_code=500)


        try:
            file =  "iris.parquet"
            blob_data = download_blob_as_stream(container_name, blob_path) 


        except Exception as e:
            logging.error(f"Error: {e}")
            return func.HttpResponse("Failed to connect to container", status_code=500)

        



        return func.HttpResponse(
            "This HTTP triggered function executed successfully",
            status_code=200
            )
    
    except Exception as e:
        return func.HttpResponse(
        f"Exception: {e}",
        status_code=500
        )
