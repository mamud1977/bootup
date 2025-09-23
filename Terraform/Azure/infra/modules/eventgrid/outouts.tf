output "eventgrid_subscription_id" {
  value = azurerm_eventgrid_event_subscription.event_subscription.id
}

output "azure_function_endpoint" {
  value = azurerm_eventgrid_event_subscription.event_subscription.azure_function_endpoint
}

