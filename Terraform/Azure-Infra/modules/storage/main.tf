
resource "azurerm_storage_account" "storage_account_name_1" {
  name                     = var.storage_account_name_1
  resource_group_name      = var.resource_group_name
  location                 = var.resource_group_location
  account_kind             = "StorageV2"
  account_tier             = "Standard"
  account_replication_type = "LRS"
  access_tier              = "Hot"


  depends_on = [azurerm_resource_group.resource_group]

  blob_properties {
    delete_retention_policy {
      days = 1 # Soft delete retention
    }

    container_delete_retention_policy {
      days = 1
    }
    versioning_enabled  = true
    change_feed_enabled = true
  }

  tags = {
    environment = "Dev"
    createdby   = "Mamud"
  }
}

resource "azurerm_storage_container" "my_container" {
  name                  = var.storage_container_name_1
  storage_account_name  = azurerm_storage_account.storage_account_name_1.name                        
  container_access_type = "private"
}
