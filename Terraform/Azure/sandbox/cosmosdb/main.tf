terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.50.0"
    }
  }
}

provider "azurerm" {
  features {}

  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id
  client_id       = var.client_id
  client_secret   = var.client_secret
}

resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.resource_group_location
}

resource "azurerm_cosmosdb_account" "cosmosdb_account" {
  name                = var.cosmosdb_account_name1

  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  geo_location {
    location          = azurerm_resource_group.rg.location
    failover_priority = 0
    zone_redundant    = false  # ✅ Correct field name and placement
  }

  capabilities {
    name = "EnableServerless"
  }

  public_network_access_enabled = true  # Allows access from all networks

  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"

  consistency_policy {
    consistency_level       = "Session"
  }

  tags = {
    environment = "sandbox"
    owner       = "Mamud"
    project     = "infra-automation"
  }
}

resource "azurerm_cosmosdb_sql_database" "cosmos_db_1" {
  name                = var.cosmosdb_database_name
  resource_group_name = azurerm_resource_group.rg.name
  account_name        = azurerm_cosmosdb_account.cosmosdb_account.name
  throughput          = null  # Required to be null for serverless
}

resource "azurerm_cosmosdb_sql_container" "container_1" {
  name                = var.cosmosdb_container_name
  resource_group_name = azurerm_resource_group.rg.name
  account_name        = azurerm_cosmosdb_account.cosmosdb_account.name
  database_name       = azurerm_cosmosdb_sql_database.cosmos_db_1.name
  partition_key_path  = "/make"
  partition_key_version = 2

  default_ttl = -1  # Documents never expire
}
