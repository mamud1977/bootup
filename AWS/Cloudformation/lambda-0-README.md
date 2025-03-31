## Invoke function synchronously

aws lambda invoke --function-name first_lambda --payload BASE64-ENCODED-STRING response.json

C:\MyWork\gitlocal\bootup\AWS\Lambda>aws lambda invoke --function-name first_lambda --payload ewogICJrZXkxIjogInZhbHVlMSIsCiAgImtleTIiOiAidmFsdWUyIiwKICAia2V5MyI6ICJ2YWx1ZTMiCn0= response.json
{
    "StatusCode": 200,
    "ExecutedVersion": "$LATEST"
}

aws lambda invoke --function-name mytestfunction out
at

## Invoke function asynchronously

aws lambda invoke --function-name mytestfunction --invocation-type Event --payload BASE64-ENCODED-STRING response.json

aws lambda invoke --function-name first_lambda --invocation-type Event --payload ewogICJrZXkxIjogInZhbHVlMSIsCiAgImtleTIiOiAidmFsdWUyIiwKICAia2V5MyI6ICJ2YWx1ZTMiCn0= response.json
------------------------------------------------

## Create Lambda function from zip file

zip function.zip index.js
tar -acf function.zip index.py

aws lambda create-function --function-name EventSourceSQS --zip-file function.zip --handler index.handler --runtime nodejs16.x --role arn:aws:iam::821711655051:role/my-sqs-role

aws lambda create-function --function-name EventSourceSQS --zip-file fileb://index.py.zip --handler index.lambda_handler --runtime python3.11 --role arn:aws:iam::418295706200:role/LambdaFunctionRole

## Create event-source mapping

aws lambda create-event-source-mapping --function-name EventSourceSQS --batch-size 10 --event-source-arn arn:aws:sqs:us-east-1:418295706200:MyQueue

aws lambda list-event-source-mappings --function-name EventSourceSQS --event-source-arn arn:aws:sqs:us-east-1:418295706200:MyQueue

aws lambda delete-event-source-mapping --uuid f52f670d-3bc7-4848-ba55-45f4f81f20f6