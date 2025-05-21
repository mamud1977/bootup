import json
import time
import boto3


def hello(event, context):
    print("Hello World")
    time.sleep(1)

    return "response"


def list_lambdas(event, context):
    client = boto3.client('lambda')
    response = client.list_functions()

    print(response)
    return response