# root main.tf

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

resource "random_string" "storage_suffix" {
  length  = 6
  upper   = false
  special = false
}


locals {
  resource_group_name       = "${var.env}-${var.resource_group_name_1}"
  resource_group_location   = "${var.resource_group_location}"

  storage_account_name      = "${var.env}${var.storage_account_name}"
  container_name            = "${var.env}-${var.container_name}"
  
  cosmosdb_account_name     = "${var.cosmosdb_account_name}-${var.env}-${random_string.storage_suffix.result}"
}

resource "azurerm_resource_group" "resource_group" {
  name     = local.resource_group_name
  location = local.resource_group_location
}

module "storage" {
  source                  = "./modules/storage"
  resource_group_name     = local.resource_group_name
  resource_group_location = local.resource_group_location

  storage_account_name    = local.storage_account_name
  container_name          = local.container_name

  depends_on = [azurerm_resource_group.resource_group]
  tags                    = var.tags

}


module "cosmosdb" {
  source                  = "./modules/cosmos-db"
  resource_group_name     = local.resource_group_name
  resource_group_location = local.resource_group_location
  cosmosdb_account_name   = local.cosmosdb_account_name

  depends_on = [azurerm_resource_group.resource_group]
  tags                    = var.tags
}


