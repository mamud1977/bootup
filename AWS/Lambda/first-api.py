import json
# Example data

data = {
    "items": [
        {"id": 1, "name": "Item 1", "price": 10.99},
        {"id": 2, "name": "Item 2", "price": 15.99},
        {"id": 3, "name": "Item 3", "price": 20.99},
    ]
}

def lambda_handler(event, context):
    # Determine the HTTP method of the request
    http_method = event["httpMethod"]
    # Handle GET request
    if http_method == "GET":
        # Return the data in the response
        response = {
            "statusCode": 200,
            "body": json.dumps(data)
        }
        return response

    # Handle POST request
    elif http_method == "POST":
        # Retrieve the request's body and parse it as JSON
        body = json.loads(event["body"])
        # Add the received data to the example data
        data["items"].append(body)
        # Return the updated data in the response
        response = {
            "statusCode": 200,
            "body": json.dumps(data)
        }
        return response

    # Handle PUT request
    elif http_method == "PUT":
        # Retrieve the request's body and parse it as JSON
        body = json.loads(event["body"])
        # Update the example data with the received data
        for item in data["items"]:
            if item["id"] == body["id"]:
                item.update(body)
                break
        # Return the updated data in the response
        response = {
            "statusCode": 200,
            "body": json.dumps(data)
        }
        return response

         # Handle DELETE request
    elif http_method == "DELETE":
        # Retrieve the request's body and parse it as JSON
        body = json.loads(event["body"])
        # Find the item with the specified id in the example data
        for i, item in enumerate(data["items"]):
            if item["id"] == body["id"]:
                # Remove the item from the example data
                del data["items"][i]
                break
        # Return the updated data in the response
        response = {
            "statusCode": 200,
            "body": json.dumps(data)
        }
        return response

    else:
        # Return an error message for unsupported methods
        response = {
            "statusCode": 405,
            "body": json.dumps({"error": "Method not allowed"})
        }
        return response