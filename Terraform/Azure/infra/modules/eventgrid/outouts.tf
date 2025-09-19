output "eventgrid_subscription_id" {
  value = azurerm_eventgrid_event_subscription.blob_created.id
}
