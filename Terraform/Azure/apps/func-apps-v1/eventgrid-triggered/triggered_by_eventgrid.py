import logging
import azure.functions as func
import json

def main(event: func.EventGridEvent):
    logging.info(f"Event Grid trigger fired: {event.id}")
    data = event.get_json()
    logging.info(f"Blob URL: {data['url']}")
    logging.info(f"whole data: {data}")