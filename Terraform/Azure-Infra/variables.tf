# variables.tf

variable "env" {
  description = "Deployment environment (e.g., dev, test, prod)"
  type        = string
}

variable "resource_group_name_1" {
  description = "Azure Resource Group Name"
  type        = string
}

variable "resource_group_location" {
  description = "Azure Resource Group Name"
  type        = string
}

variable "storage_account_name_1" {
  description = "Azure Storage Account Name"
  type        = string
}

variable "storage_container_name_1" {
  description = "Name of the blob container"
  type        = string
}

variable "cosmosdb_account_name " {
  description = "Name of the cosmosdb account"
  type        = string
}
