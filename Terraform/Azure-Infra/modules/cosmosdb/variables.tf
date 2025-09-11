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
