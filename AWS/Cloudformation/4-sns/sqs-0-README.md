## AWS SQS CLI Commands

aws sqs list-queues

C:\MyWork\gitlocal\bootup\AWS\Lambda>aws sqs list-queues
{
    "QueueUrls": [
        "https://sqs.us-east-1.amazonaws.com/418295706200/dev-FIFOQueue1.fifo",
        "https://sqs.us-east-1.amazonaws.com/418295706200/dev-StandardQueue1"
    ]
}

=========================================

aws sqs get-queue-attributes --queue-url "https://sqs.us-east-1.amazonaws.com/418295706200/dev-StandardQueue1" --attribute-names All



=========================================

aws sqs send-message --queue-url QUEUE-URL --message-body test-message-1 --delay-seconds 10

aws sqs send-message --queue-url "https://sqs.us-east-1.amazonaws.com/418295706200/dev-StandardQueue1" --message-body test-message-1 --delay-seconds 2


C:\MyWork\gitlocal\bootup\AWS\Lambda>aws sqs send-message --queue-url "https://sqs.us-east-1.amazonaws.com/418295706200/dev-FIFOQueue1.fifo" --message-body test-message-1 --message-group-id "group1" --message-deduplication-id "message1"
{
    "MD5OfMessageBody": "d97fd90db5ae99ec5cfa7821d8b44e3e",
    "MessageId": "8a6587d7-3a2c-492e-b19d-97350b119e3f",
    "SequenceNumber": "18893074667213295872"
}



=========================================
aws sqs receive-message --queue-url QUEUE-URL --wait-time-seconds 10


=========================================
aws sqs send-message --queue-url QUEUE-URL --message-body test-long-short-polling