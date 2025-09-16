# module apim/variables.tf

variable "random_string" {}

variable "apim_name" {}
variable "resource_group_name" {}
variable "resource_group_location" {}
variable "publisher_name" {}
variable "publisher_email" {}
variable "sku_name" {}
variable "tags" {}
variable "env" {}
variable "function_app_hostname" {}
variable "function_key" {
  type      = string
  sensitive = true
}

variable "identity {}