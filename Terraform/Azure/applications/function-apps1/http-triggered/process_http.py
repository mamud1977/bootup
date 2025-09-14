import logging
import azure.functions as func
from rapidfuzz import fuzz, process


def main(req: func.HttpRequest) -> func.HttpResponse:
    
    input_po_num = req.params.get("po_number")

    choices = ["PO 12345", "POx 83n333", "PO 383838302"]

    #Find top 3 matches
    matches = process.extract(input_po_num, choices, limit=3)
    print("Top matches:")
    for match in matches:
        print(match)


    if name:
        logging.info(f"Query parameter 'po_number' is present: {po_number}")
    else:
        logging.info("Query parameter 'po_number' is not present.")

    try:
        req_body = req.get_json()
        logging.info(f"Request body received: {req_body}")
    except ValueError:
        logging.info("No valid JSON body received.")

    return func.HttpResponse("Request processed.", status_code=200)



