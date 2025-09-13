variable "resource_group_name" {
  description = "Azure Resource Group Name"
  type        = string
}

variable "resource_group_location" {
  description = "Azure Resource Group Name"
  type        = string
}


variable "cosmosdb_account_name" {
  type        = string
  description = "Cosmos DB account name"
}

variable "offer_type" {
  type        = string
  default     = "Standard"
}

variable "kind" {
  type        = string
  default     = "GlobalDocumentDB" # For SQL API
}
