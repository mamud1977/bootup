import json

def lambda_handler(event, context):
    order = json.loads(event['body'])
    return  json.dump({"statusCode" : 201, "headers" : {}, "body" : "Orders created"})


