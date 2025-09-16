# infra/apim/main.tf

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
    key                  = "apim.terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

data "terraform_remote_state" "infra" {
  backend = "azurerm"
  config = {
    resource_group_name  = "rg-dev-sandbox-tfstate"
    storage_account_name = "tfstatehellomamud1977"
    container_name       = "tfstate-dev"
    key                  = "dev.terraform.tfstate"
  }
}

## APIM Resource
#resource "azurerm_api_management" "apim" {
#  name                = "apim-2-${data.terraform_remote_state.infra.outputs.env}-${data.terraform_remote_state.infra.outputs.random_string}"
#  location            = data.terraform_remote_state.infra.outputs.resource_group_location
#  resource_group_name = data.terraform_remote_state.infra.outputs.resource_group_name
#  publisher_name      = "By Mamud"
#  publisher_email     = "mamud1977@outlook.com"
#  sku_name            = "Developer_1"
#
#  identity {
#    type = "SystemAssigned"
#  }
#
#  tags = data.terraform_remote_state.infra.outputs.tags
#}

locals {
  env                     = data.terraform_remote_state.infra.outputs.env
  random_string           = data.terraform_remote_state.infra.outputs.random_string
  resource_group_name     = data.terraform_remote_state.infra.outputs.resource_group_name
  resource_group_location = data.terraform_remote_state.infra.outputs.resource_group_location

  apim_name               = "${var.apim_name}-${env}-${random_string}"
  tags                    = data.terraform_remote_state.infra.outputs.tags
}


##########  3. Create an APIM

resource "azurerm_api_management" "apim" {
  name                = local.apim_name

  location            = local.resource_group_location
  resource_group_name = local.resource_group_name
  
  publisher_name      = var.publisher_name
  publisher_email     = var.publisher_email
  sku_name            = var.sku_name

  identity {
    type = "SystemAssigned"
  }

  tags = local.tags
}


