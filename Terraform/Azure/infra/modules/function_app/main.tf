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

