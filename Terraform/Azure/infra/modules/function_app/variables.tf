variable "resource_group_name" {}
variable "resource_group_location" {}
variable "function_app_name" {}
variable "plan_name" {}
variable "storage_account_name" {}
variable "storage_account_access_key" {}
variable "storage_connection_string" {}
variable "tags" {
  type = map(string)
}
