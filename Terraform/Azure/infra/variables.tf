# variables.tf

variable "env" {
  description = "Deployment environment (e.g., dev, test, prod)"
  type        = string
}

variable "tags" {
  type        = map(string)
  description = "Standard tags to apply to all resources"
}

variable "resource_group_name_1" {
  description = "Azure Resource Group Name"
  type        = string
}

variable "resource_group_location" {
  description = "Azure Resource Group Name"
  type        = string
}

variable "storage_account_name" {
  description = "Azure Storage Account Name"
  type        = string
}

variable "container_name" {
  description = "Name of the blob container"
  type        = string
}