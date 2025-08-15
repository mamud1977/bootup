from snowflake_connector import connect
import logging
import json


if logging.getLogger().hasHandlers():
    # AWS Lambda Logger
    logging.getLogger().setLevel(logging.INFO)
else:
    # Local Logger
    logging.basicConfig(
        format="%(name)s: %(asctime)s - %(message)s",
        datefmt="%y-%d-%m %H:%M:%S",
        level=logging.INFO,
    )

with open('event_apigateway.json', 'r') as file:
    event = json.load(file)
    #print(event) 


def parse_params(event: dict) -> dict:
    path_body = event.get("pathParameters")
    path_parameters = path_body if path_body else {}

    query_body = event.get("queryStringParameters")
    query_params = query_body if query_body else {}

    request_body = event.get("body")
    request_params = json.loads(request_body) if request_body else {}

    # loop through request params
    # if value.lower = "null" -> None ; handles commented out / null config
    # if value.lower = "'null_'" -> value.strip(_) ; handles where value should be null string
    if "null" in str(request_params.values()).lower():
        for key, value in request_params.items():
            if isinstance(value, str) and value.lower() == "null":
                request_params[key] = None

    if "null_" in str(request_params.values()).lower():
        for key, value in request_params.items():
            if isinstance(value, str) and value.lower() == "null_":
                request_params[key] = value.strip("_")

    params = {**path_parameters, **query_params, **request_params}

    # Setup Static Values
    params["domain"] = event["requestContext"]["domainName"]
    params["stage"] = event["requestContext"]["stage"]
    params["base_url"] = f"https://{params['domain']}/{params['stage']}"
    params["api_key_id"] = event["requestContext"]["identity"]["apiKeyId"]

    params["auth_headers"] = {
        "x-api-key": event["headers"]["x-api-key"],
        "Authorization": event["headers"]["Authorization"],
    }

    logging.info(f"Parsed the following params from the incoming request: {params}")

    return params


QUERY_IDS = {}

print('Test utils...')

conn = connect()

# print(conn)

query_params = parse_params(event)

print(query_params)

# # Validate If Process Actually Exists
# results = db.execute_template_query(
#     snowflake_connector,
#     template_name="get_existing_sets",
#     query_params=query_params,
#     template_path=C.LAMBDA_LAYER_PATH,
#     )

    