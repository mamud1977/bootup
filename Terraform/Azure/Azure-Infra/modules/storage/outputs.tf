output "storage_account_name" {
  value = azurerm_storage_account.storage_account.name
}

output "storage_account_id" {
  value = azurerm_storage_account.storage_account.id
}

output "primary_access_key" {
  value = azurerm_storage_account.storage_account.primary_access_key
  sensitive = true
}

output "storage_connection_string" {
  value = azurerm_storage_account.storage_account.primary_connection_string
}

output "container_name" {
  value = azurerm_storage_container.my_container.name
}

output "container_id" {
  value = azurerm_storage_container.my_container.id
}

