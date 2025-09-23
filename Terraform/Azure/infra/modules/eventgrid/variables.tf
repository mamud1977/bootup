variable "subscription_name" {}
variable "storage_account_id" {}
variable "function_app_id" {}

variable "function_name_eventgrid_triggered" {
  description = "Name of azure function"
  type        = string
  default     = "eventgrid-triggered"
}

variable "dead_letter_container_name" {}

variable "labels" {}

