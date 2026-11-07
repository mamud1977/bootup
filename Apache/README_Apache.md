cd C:\MySoftware\terraform
terraform -chdir=apache-kafka-local init
terraform -chdir=apache-kafka-local plan -out=tfplan
terraform -chdir=apache-kafka-local apply tfplan
terraform -chdir=apache-kafka-local destroy

