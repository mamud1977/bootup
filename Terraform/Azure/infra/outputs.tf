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

