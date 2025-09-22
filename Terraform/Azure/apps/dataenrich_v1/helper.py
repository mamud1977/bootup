import re
import os
import json
import logging


def dump_json(json_input):
    """
    Processes a dictionary representing JSON input to extract and format specific information,
    then converts the processed data back into a JSON string.

    The function expects the input dictionary to potentially contain keys such as
    'companyAddress', 'deliveryAddress', 'contact', 'sender', 'companyRegistrationNumber',
    and 'documentType'. It extracts relevant details from these sections, performs
    some data cleaning and transformation, and combines them into a new dictionary
    structure.

    Args:
        json_input: A dictionary representing the JSON input. It is expected to have
            at least 'companyAddress' and 'deliveryAddress' keys, though their
            values can be empty dictionaries.

    Returns:
        A tuple containing two elements:
            - A JSON formatted string (with indentation for readability) of the
              processed address information, including company name, registration number,
              company address details (excluding 'name'), delivery address details
              (excluding 'name'), contact email, and sender email.
            - An uppercase string of the 'documentType' with any whitespace removed.

    Raises:
        KeyError: If the input `json_input` does not contain the keys 'companyAddress'
            or 'deliveryAddress'.
    """
        
    # Ensure required keys exist in the input JSON

    logging.info(f"dump_json: Processing started here ...")

    company_address_with_null = {
        key: value for key, value in json_input.get("companyAddress", {}).items() if key != "name"
        }
    delivery_address_with_null = {
        key: value for key, value in json_input.get("deliveryAddress", {}).items() if key != "name"
        }
    contact_email = json_input.get('contact', {}).get('email')
    sender_email = json_input.get('sender', {}).get('email')
    company_reg_number = json_input.get('companyRegistrationNumber', "").replace(" ", "")
    document_type = "".join(json_input.get('documentType', "").split()).upper()

    if not delivery_address_with_null:
        raise KeyError("The input JSON must contain a 'deliveryAddress' key.")
    
    if not company_address_with_null:
        raise KeyError("The input JSON must contain a 'companyAddress' key.")

    ## Add email to delivery address
    #delivery_address_with_null["email"] = contact_email

    company_name=""
    # Check if companyName is empty
    if not json_input.get('companyName'):
        # Try to fill with companyAddress name
        if json_input.get('companyAddress', {}).get('name'):
            company_name = json_input['companyAddress']['name']
        # If companyAddress name is not available, try deliveryAddress name
        elif json_input.get('deliveryAddress', {}).get('name'):
            company_name = json_input['deliveryAddress']['name']
    else:
        company_name =  json_input.get('companyName')



        # Combine the processed addresses into a single dictionary
    processed_addresses = {
            "companyName": company_name,
            "companyRegistrationNumber": company_reg_number,
            "companyAddress": company_address_with_null,
            "deliveryAddress": delivery_address_with_null,
            "contact_email": contact_email,
            "sender_email": sender_email
    }

    # Convert the processed delivery address to a JSON string
    json_dump = json.dumps(processed_addresses, indent=4)
    return json_dump, document_type


    
