terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.50.0"
    }
  }


  backend "azurerm" {
    resource_group_name  = "rg-dev-sandbox-tfstate"
    storage_account_name = "tfstatehellomamud1977"
    container_name       = "tfstate-dev"
    key                  = "dev.terraform.tfstate"
  }
}


provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "resource_group" {
  name     = var.resource_group_name_1
  location = var.resource_group_location
}

resource "azurerm_storage_account" "storage_account_name_1" {
  name                     = var.storage_account_name_1
  resource_group_name      = azurerm_resource_group.resource_group.name
  location                 = azurerm_resource_group.resource_group.location
  account_kind             = "StorageV2"
  account_tier             = "Standard"
  account_replication_type = "LRS"
  access_tier              = "Hot"

  blob_properties {
    delete_retention_policy {
      days = 1 # Soft delete retention
    }

    container_delete_retention_policy {
      days = 1
    }
    versioning_enabled  = true
    change_feed_enabled = true
  }

  tags = {
    environment = "Dev"
    createdby   = "Mamud"
  }
}

