output "eventgrid_subscription_id" {
  value = azurerm_eventgrid_event_subscription.eventgrid_triggerd.id
}

output "azure_function_endpoint" {
  value = azurerm_eventgrid_event_subscription.eventgrid_triggerd.azure_function_endpoint
}

