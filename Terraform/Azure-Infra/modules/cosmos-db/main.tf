resource "azurerm_cosmosdb_account" "cosmosdb_account" {
  name                = var.cosmosdb_account_name
  resource_group_name = var.resource_group_name
  location            = var.resource_group_location
  
  offer_type          = var.offer_type
  kind                = var.kind

  consistency_policy {
    consistency_level       = "Session"
  }

  geo_location {
    location          = var.resource_group_location
    failover_priority = 0
  }

  capabilities {
    name = "EnableServerless" # Optional: remove if not needed
  }
}

