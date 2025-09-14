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
  resource_group_name     = "${var.resource_group_name_1}-${var.env}"
  resource_group_location = "${var.resource_group_location}"

  storage_account_name    = "${var.storage_account_name}${var.env}"
  container_name          = "${var.container_name}-${var.env}"
  
  cosmosdb_account_name   = "${var.cosmosdb_account_name}-${var.env}-${random_string.storage_suffix.result}"

  function_app_name       = "Function-App-${var.env}-${random_string.storage_suffix.result}"
  plan_name               = "$function-plan-{var.env}"

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
  tags                    = var.tags

  depends_on = [azurerm_resource_group.resource_group]
}


module "cosmosdb" {
  source                  = "./modules/cosmos-db"
  resource_group_name     = local.resource_group_name
  resource_group_location = local.resource_group_location
  cosmosdb_account_name   = local.cosmosdb_account_name
  tags                    = var.tags

  depends_on = [azurerm_resource_group.resource_group]
}

module "function_app" {
  source                  = "./modules/function_app"
  resource_group_name     = local.resource_group_name
  resource_group_location = local.resource_group_location
  function_app_name       = local.function_app_name
  plan_name               = "${var.env}-func-plan"
  storage_account_name    = module.storage.storage_account_name
  tags                    = var.tags

  depends_on = [azurerm_resource_group.resource_group]
}







