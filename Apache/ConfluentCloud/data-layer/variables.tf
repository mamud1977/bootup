############################################
# data layer : variables.tf
############################################

variable "environment_name" {
  type    = string
}

variable "confluent_api_key" {
  description = "Confluent Cloud API Key"
  type        = string
  sensitive   = true
}

variable "confluent_api_secret" {
  description = "Confluent Cloud API Secret"
  type        = string
  sensitive   = true
}


########################################################
# Snowflake Source Connector for Apache Kafka:
########################################################

variable "snowflake_private_key" {
  type      = string
  sensitive = true
}

variable "snowflake_user" {
  type = string
}

variable "snowflake_url" {
  type = string
}

variable "aws_access_key" {
  type = string
}

variable "aws_secret_access_key" {
  type = string
}

