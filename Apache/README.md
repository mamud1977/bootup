
### Terraform Code for ConfluentClod Environment setup

cd C:\Users\Mamud\Gitlocal\bootup\Apache\Terraform\ConfluentCloud

terraform init

set KAFKA_API_KEY=
set KAFKA_API_SECRET=
set KAFKA_REST_ENDPOINT=

terraform plan -out=tfplan
terraform apply tfplan
terraform destroy

### In Windows

cd C:\Users\Mamud\Gitlocal\bootup\Apache
python -m venv .venv
.\.venv\Scripts\activate.bat

pip install -r requirements.txt

set KAFKA_API_KEY=<>
set KAFKA_API_SECRET=<>
set KAFKA_BOOTSTRAP_SERVERS=<>

uvicorn Application.producer:app --port 8000 --reload 

### To Kill Uvicorn

netstat -ano | findstr :8000
  TCP    127.0.0.1:8000         0.0.0.0:0              LISTENING       5484

taskkill /PID 8440 /F



### Standalone Kafka Consumer

# Run it like this:

python -m Application.consumer

# Stop it like this:

CTRL + C