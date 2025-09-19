output "env" {
  value = var.env
}

output "tags" {
  value = var.tags
}

output "random_string" {
  value = random_string.storage_suffix.result
}

output "resource_group_name" {
  value = azurerm_resource_group.resource_group.name
}

output "resource_group_location" {
  value = azurerm_resource_group.resource_group.location
}

################### Storage related outputs

output "storage_account_name" {
  value = azurerm_storage_account.storage_account.name
}

output "storage_account_id" {
  value = azurerm_storage_account.storage_account.id
}

output "primary_access_key" {
  value = module.storage.primary_access_key
  sensitive = true
}

output "primary_connection_string" {
  value = module.storage.primary_connection_string
}

output "container_name" {
  value = module.storage.container.name
}

output "container_id" {
  value = module.storage.container.id
}

output "parquet_container_name" {
  value = module.storage.parquet_container_name
}

################### Function App related outputs

output "function_app_id" {
  value = module.function_app.function_app_id

}

################### Event Grid related outputs

output "eventgrid_subscription_id" {
  value = module.eventgrid.eventgrid_subscription_id
}

