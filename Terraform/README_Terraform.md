To check if Terraform is installed on your WSL Ubuntu instance, open your Ubuntu terminal within WSL and execute the following command:

terraform --version

terraform init
terraform plan
terraform apply
terraform apply -refresh-only
terraform show
terraform destroy
terraform output
terraform validate


When running Terraform locally in VS Code, you can set environment variables in your terminal. For Terraform to recognize them, the environment variable names must be prefixed with TF_VAR_ followed by the variable name from your variables.tf file.

export TF_VAR_some_api_key="your_vscode_api_key"
export TF_VAR_database_password="your_vscode_db_password"


