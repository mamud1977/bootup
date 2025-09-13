variable "resource_group_name" {}
variable "resource_group_location" {}
variable "function_app_name" {}
variable "plan_name" {}
variable "storage_account_name" {}
variable "tags" {
  type = map(string)
}
