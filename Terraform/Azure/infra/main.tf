# root/main.tf

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

  function_app_name       = "function-app-${var.env}-${random_string.storage_suffix.result}"
  plan_name               = "function-app-plan-${var.env}"

}

resource "azurerm_resource_group" "resource_group" {
  name     = local.resource_group_name
  location = local.resource_group_location
}

resource "azurerm_log_analytics_workspace" "log_analytics" {
  name                = "log-analytics-${var.env}"
  location            = local.resource_group_location
  resource_group_name = local.resource_group_name
  sku                 = "PerGB2018"
  retention_in_days   = 30

  depends_on = [azurerm_resource_group.resource_group]
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
  source                        = "./modules/function_app"
  resource_group_name           = local.resource_group_name
  resource_group_location       = local.resource_group_location
  function_app_name             = local.function_app_name
  plan_name                     = local.plan_name

  storage_account_name          = module.storage.storage_account_name
  storage_connection_string     = module.storage.storage_connection_string
  storage_account_access_key    = module.storage.primary_access_key
  
  tags                          = var.tags
  

  log_analytics_workspace_id = azurerm_log_analytics_workspace.log_analytics.id

  depends_on                    = [
                                  azurerm_resource_group.resource_group,
                                  azurerm_log_analytics_workspace.log_analytics]
}


module "apim" {
  source                  = "./modules/apim"
  resource_group_name     = local.resource_group_name
  resource_group_location = local.resource_group_location

  apim_name               = "apim-${var.env}-${random_string.storage_suffix.result}"
  publisher_name          = "ByMamud"
  publisher_email         = "mamud1977@outlook.com"
  sku_name                = "Developer_1"  # Use Standard_1 or Premium_1 for production

  tags                    = var.tags
  env                     = var.env
  function_app_hostname   = module.function_app.function_app_hostname
  function_key            = module.function_app.function_key
  depends_on = [azurerm_resource_group.resource_group]
}







