# modules/function_app/main.tf


resource "azurerm_service_plan" "plan" {
  name                = var.plan_name
  location            = var.resource_group_location
  resource_group_name = var.resource_group_name
  os_type             = "Linux"
  sku_name            = "Y1" # Free tier (Consumption)
  tags                = var.tags
}

resource "azurerm_application_insights" "insights" {
  name                = "${var.function_app_name}-app-insight"
  location            = var.resource_group_location
  resource_group_name = var.resource_group_name
  application_type    = "web"

  workspace_id        = var.log_analytics_workspace_id
}


resource "azurerm_linux_function_app" "function_app" {
  name                       = var.function_app_name
  location                   = var.resource_group_location
  resource_group_name        = var.resource_group_name
  
  service_plan_id            = azurerm_service_plan.plan.id
  
  storage_account_name       = var.storage_account_name
  storage_account_access_key = var.storage_account_access_key



  functions_extension_version = "~4"

  site_config {
    application_stack {
      python_version = "3.10"
    }
  }

  app_settings = {
    FUNCTIONS_WORKER_RUNTIME        = "python"
    AzureWebJobsStorage             = var.storage_connection_string
    APPINSIGHTS_INSTRUMENTATIONKEY = azurerm_application_insights.insights.instrumentation_key
  }


  identity {
    type = "SystemAssigned"
  }

  tags = var.tags
}

data "azurerm_function_app_host_keys" "function_key" {
  name                = azurerm_linux_function_app.function_app.name
  resource_group_name = var.resource_group_name
  depends_on          = [azurerm_linux_function_app.function_app]
}