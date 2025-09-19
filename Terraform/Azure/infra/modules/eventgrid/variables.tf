variable "subscription_name" {}
variable "storage_account_id" {}
variable "function_app_id" {}

variable "function_name-blob-triggered" {
  description = "Name of azure function"
  type        = string
  default     = "blob-triggered"
}

variable "labels" {}

