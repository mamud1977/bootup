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


resource "azurerm_resource_group" "rg-sandbox1" {
  name     = var.resource_group1_name
  location = "East US"
}

resource "azurerm_storage_account" "stgacct1977" {
  name                      = var.storage_account_name1
  resource_group_name       = azurerm_resource_group.rg-sandbox1.name
  location                  = azurerm_resource_group.rg-sandbox1.location
  account_kind              = "StorageV2"
  account_tier              = "Standard"
  account_replication_type  = "LRS"
  access_tier               = "Hot"
 
  blob_properties {
    delete_retention_policy {
      days = 1  # Soft delete retention
    }

    container_delete_retention_policy {
        days = 1
      }
    versioning_enabled = true
    change_feed_enabled = true
  }


  tags = {
    environment = "dev"
  }
}
