# -------------------------------------------------
# Confluent Cloud : Infra-layer

cd C:\MyWork\gitlocal\bootup\Apache\ConfluentCloud\infra-layer

terraform init
terraform plan -out=tfplan
terraform apply tfplan
terraform destroy -auto-approve

# -------------------------------------------------
# Confluent Cloud : data-layer

cd C:\MyWork\gitlocal\bootup\Apache\ConfluentCloud\data-layer

terraform init
terraform plan -out=tfplan
terraform apply tfplan
terraform destroy -auto-approve