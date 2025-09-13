variable "env" {
  type        = string
  description = "Environment name (e.g., dev, prod)"
}

variable "resource_group_name" {
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
