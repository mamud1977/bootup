# -------------------------------------------------
# Application : Producer

cd C:\MyWork\gitlocal\bootup\Apache\Application


terraform output -raw bootstrap_endpoint
terraform output -raw sa_api_key
terraform output -raw sa_api_secret
terraform output -raw schema_registry_endpoint
terraform output -raw schema_registry_api_key
terraform output -raw schema_registry_api_secret



set KAFKA_BOOTSTRAP_SERVERS=pkc-oxqxx9.us-east-1.aws.confluent.cloud:9092

set KAFKA_API_KEY= <>

set KAFKA_API_SECRET= <>

set SCHEMA_REGISTRY_URL=https://psrc-40q7p6o.us-east-1.aws.confluent.cloud

set SCHEMA_REGISTRY_API_KEY= <>

set SCHEMA_REGISTRY_API_SECRET= <>

echo %KAFKA_BOOTSTRAP_SERVERS%
echo %KAFKA_API_KEY%
echo %KAFKA_API_SECRET%
echo %SCHEMA_REGISTRY_URL%
echo %SCHEMA_REGISTRY_API_KEY%
echo %SCHEMA_REGISTRY_API_SECRET%

python -m venv .venv
.\.venv\Scripts\activate.bat
pip install -r requirements.txt
uvicorn producer:app --reload --port 8000
http://127.0.0.1:8000/docs


# -------------------------------------------------
# Application : Consumer

cd C:\MyWork\gitlocal\bootup\Apache\Application

# from Infra-layer
set KAFKA_BOOTSTRAP_SERVERS=pkc-oxqxx9.us-east-1.aws.confluent.cloud:9092

set KAFKA_API_KEY= <>

set KAFKA_API_SECRET= <>

set SCHEMA_REGISTRY_URL=https://psrc-40q7p6o.us-east-1.aws.confluent.cloud

set SCHEMA_REGISTRY_API_KEY= <>

set SCHEMA_REGISTRY_API_SECRET= <>


python -m venv .venv
.\.venv\Scripts\activate.bat
pip install -r requirements.txt
uvicorn consumer:app --reload --port 8001