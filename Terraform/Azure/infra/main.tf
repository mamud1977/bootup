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
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}

resource "random_string" "storage_suffix" {
  length  = 6
  upper   = false
  special = false
}



locals {
  env                     = var.env
  resource_group_name     = "${var.resource_group_name_1}-${var.env}"
  resource_group_location = "${var.resource_group_location}"

  storage_account_name    = "${var.storage_account_name}${var.env}"
  container_name          = "${var.container_name}-${var.env}"
  
  function_app_v1_name       = "function-app-v1-${var.env}-${random_string.storage_suffix.result}"
  function_app_v2_name       = "function-app-v2-${var.env}-${random_string.storage_suffix.result}"
  plan_name                  = "function-app-plan-${var.env}"

}

resource "azurerm_resource_group" "resource_group" {
  name     = local.resource_group_name
  location = local.resource_group_location
}


module "monitoring" {
  source                  = "./modules/monitoring"
  env                     = local.env
  resource_group_name     = local.resource_group_name
  resource_group_location = local.resource_group_location
  tags                    = var.tags

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

module "function_app" {
  source                     = "./modules/function_app"
  env                        = local.env
  resource_group_name        = local.resource_group_name
  resource_group_location    = local.resource_group_location
  
  function_app_name          = local.function_app_v1_name
  plan_name                  = local.plan_name

  storage_account_name       = module.storage.storage_account_name
  storage_connection_string  = module.storage.primary_connection_string
  storage_account_access_key = module.storage.primary_access_key
  
  tags                       = var.tags
 
  application_insights_id    = module.monitoring.application_insights_id
  instrumentation_key        = module.monitoring.instrumentation_key
  
  depends_on                    = [
                                  azurerm_resource_group.resource_group,
                                  module.monitoring,
                                  module.storage
                                  ]
}

module "function_app" {
  source                     = "./modules/function_app"
  env                        = local.env
  resource_group_name        = local.resource_group_name
  resource_group_location    = local.resource_group_location
  
  function_app_name          = local.function_app_v2_name
  plan_name                  = local.plan_name

  storage_account_name       = module.storage.storage_account_name
  storage_connection_string  = module.storage.primary_connection_string
  storage_account_access_key = module.storage.primary_access_key
  
  tags                       = var.tags
 
  application_insights_id    = module.monitoring.application_insights_id
  instrumentation_key        = module.monitoring.instrumentation_key
  
  depends_on                    = [
                                  azurerm_resource_group.resource_group,
                                  module.monitoring,
                                  module.storage
                                  ]
}



module "eventgrid" {
  source              = "./modules/eventgrid"
  subscription_name   = "BlobCreated"
  storage_account_id  = module.storage.storage_account_id
  function_app_id     = module.function_app.function_app_id
  labels              = ["txt/parquet", "blob", "trigger"]
  depends_on          = [
                          module.storage, 
                          module.function_app
                        ]
        
}



