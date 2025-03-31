C:\Users\mamud>aws s3 mb s3://test-bucket-1sdx02ds0xjx
make_bucket: test-bucket-1sdx02ds0xjx


C:\Users\mamud>aws s3 ls
2025-02-25 17:00:19 cf-templates--2rcmiqxf4kkp-us-east-1
2025-02-08 12:55:58 cf-templates-q1eb0g0q32b1-us-east-1
2025-03-14 15:45:43 cf-templates-q1eb0g0q32b1-us-east-2
2025-03-29 09:01:27 events-123x
2025-03-28 16:29:26 logging-bucket-578ouu
2025-03-28 16:29:41 main-bucket-0kjt879gl
2025-03-29 10:51:15 test-bucket-1sdx02ds0xjx

C:\Users\mamud\Downloads>aws s3 cp IMG-20250111-WA0004.jpg s3://test-bucket-1sdx02ds0xjx
upload: .\IMG-20250111-WA0004.jpg to s3://test-bucket-1sdx02ds0xjx/IMG-20250111-WA0004.jpg




C:\Users\mamud>aws s3api head-object --bucket "events-k8gk754" --key "Una Paloma Blanca.pdf"
{
    "AcceptRanges": "bytes",
    "LastModified": "2025-03-27T23:44:16+00:00",
    "ContentLength": 170325,
    "ETag": "\"95b59e5a9d60ec344a5b77af00a15259\"",
    "VersionId": "6Y1arIfWuHjg4KO_KSdkk57.Rewm5R6d",
    "ContentType": "application/pdf",
    "ServerSideEncryption": "AES256",
    "Metadata": {},
    "ReplicationStatus": "PENDING"
}


C:\Users\mamud>aws s3api get-bucket-logging --bucket main-bucket-0kjt879gl
{
    "LoggingEnabled": {
        "TargetBucket": "logging-bucket-578ouu",
        "TargetPrefix": "testing-logs"
    }
}


C:\Users\mamud>aws s3 presign s3://events-123x/bce33107-b143-4327-b197-dea840b6660d.jpg
https://events-123x.s3.us-east-1.amazonaws.com/bce33107-b143-4327-b197-dea840b6660d.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAWCZC56JMICJWIA7Q%2F20250329%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250329T141101Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=365f66e93ff8d90485db85681a15c0ada6ccfc9095a0c691addf7ea87af2073a