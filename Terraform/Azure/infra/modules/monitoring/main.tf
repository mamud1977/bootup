  source                  = "./modules/monitoring"
  env                     = local.env
  resource_group_name     = local.resource_group_name
  resource_group_location = local.resource_group_location
  tags                    = var.tags

resource "azurerm_log_analytics_workspace" "log_analytics" {
  name                = "log-analytics-${var.env}"
  resource_group_name = var.resource_group_name
  location            = var.resource_group_location
  sku                 = "PerGB2018"
  retention_in_days   = 30

  tags                    = var.tags
}

resource "azurerm_application_insights" "app_insights" {
  env                 = var.env
  location            = var.resource_group_location
  resource_group_name = var.resource_group_name
  application_type    = "web"

  workspace_id        = azurerm_log_analytics_workspace.log_analytics.id

  tags                    = var.tags

  depends_on = [azurerm_log_analytics_workspace.log_analytics]
}
