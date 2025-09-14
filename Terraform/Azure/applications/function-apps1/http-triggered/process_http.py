import logging
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get("name")
    if name:
        logging.info(f"Query parameter 'name' is present: {name}")
    else:
        logging.info("Query parameter 'name' is not present.")

    try:
        req_body = req.get_json()
        logging.info(f"Request body received: {req_body}")
    except ValueError:
        logging.info("No valid JSON body received.")

    return func.HttpResponse("Request processed.", status_code=200)
