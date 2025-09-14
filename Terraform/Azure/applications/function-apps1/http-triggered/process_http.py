import logging
import azure.functions as func
from rapidfuzz import fuzz, process


def main(req: func.HttpRequest) -> func.HttpResponse:
    
    try:
        input_po_num = req.params.get("po_number")

        choices = ["PO 12345", "POx 83n333", "PO 383838302"]

        #Find top 3 matches
        matches = process.extract(input_po_num, choices, limit=3)
        print("Top matches:")
        logging.info(f"Top matches:")
        for match in matches:
            print(match)
            logging.info(f"match:{match}")

        return func.HttpResponse("Request processed.", status_code=200)
    
    except Exception as e:
        return func.HttpResponse(f"Exception: {e}", status_code=500) 



