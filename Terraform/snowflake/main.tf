terraform {
  required_providers {
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~> 0.79.0"
    }
  }
}

# Snowflake Provider Configuration : 
#This block tells Terraform how to connect to your Snowflake instance.


provider "snowflake" {
  account   = var.snowflake_account
  user      = var.snowflake_username
  role      = var.snowflake_role
  authenticator = "JWT"
  private_key = var.snowflake_private_key
}

resource "snowflake_database" "example_db" {
  name            = "MY_TERRAFORM_DB"
  comment         = "Database created via Terraform"
  data_retention_time_in_days = 1
}





