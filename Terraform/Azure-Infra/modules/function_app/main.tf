# module function_app/main.tf 


resource "azurerm_service_plan" "plan" {
  name                = var.plan_name
  location            = var.resource_group_location
  resource_group_name = var.resource_group_name
  os_type             = "Linux"
  sku_name            = "Y1" # Free tier (Consumption)
  tags                = var.tags
}

resource "azurerm_linux_function_app" "func" {
  name                       = var.function_app_name
  location                   = var.resource_group_location
  resource_group_name        = var.resource_group_name
  service_plan_id            = azurerm_app_service_plan.plan.id
  storage_account_name       = var.storage_account_name
  storage_account_access_key = data.azurerm_storage_account.primary_key.primary_access_key
  functions_extension_version = "~4"

  site_config {
    application_stack {
      python_version = "3.10"
    }
  }

  identity {
    type = "SystemAssigned"
  }

  tags = var.tags
}

data "azurerm_storage_account" "primary_key" {
  name                = var.storage_account_name
  resource_group_name = var.resource_group_name
}
