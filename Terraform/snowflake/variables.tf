variable "snowflake_account" {
  description = "The Snowflake account identifier."
  type        = string
}

variable "snowflake_username" {
  description = "The Snowflake user for Terraform to authenticate as."
  type        = string
}

variable "snowflake_role" {
  description = "The role for Terraform to use."
  type        = string
}

variable "snowflake_private_key_path" {
  description = "Path to the Snowflake private key file. Set via environment variable in CI/CD."
  type        = string
  sensitive   = true
}