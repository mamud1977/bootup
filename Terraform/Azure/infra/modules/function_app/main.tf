# modules/function_app/main.tf


resource "azurerm_service_plan" "plan" {
  name                = var.plan_name
  location            = var.resource_group_location
  resource_group_name = var.resource_group_name
  os_type             = "Linux"
  sku_name            = "Y1" # Free tier (Consumption)
  tags                = var.tags
}

resource "azurerm_linux_function_app" "function" {
  name                       = var.function_app_name
  resource_group_name        = var.resource_group_name
  location                   = var.resource_group_location
  
  service_plan_id            = azurerm_service_plan.plan.id
  storage_account_name       = var.storage_account_name
  storage_account_access_key = var.storage_account_access_key

  site_config {
    application_stack {
      python_version = "3.10"
    }
  }

  app_settings = {
    FUNCTIONS_WORKER_RUNTIME = "python"
    APPINSIGHTS_INSTRUMENTATIONKEY = var.instrumentation_key
    AzureWebJobsStorage = var.storage_connection_string
    WEBSITE_RUN_FROM_PACKAGE        = "1"
    ENV = var.env
  }

  identity {
    type = "SystemAssigned"
  }

  tags = var.tags
}

