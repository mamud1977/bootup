############################################
# infra : variables.tf
############################################

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

variable "environment_name" {
  type    = string
  default = "terraform-env"
}

variable "cluster_name" {
  type    = string
  default = "terraform-cluster"
}

variable "cloud" {
  type    = string
  default = "AWS"
}

variable "region" {
  type    = string
  default = "us-east-1"
}


variable "flink_compute_pool_name" {
  type    = string
  default = "sql-course"
}

variable "max_cfu" {
  type    = number
  default = 5
}

