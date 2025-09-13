# storage module -> main.tf
locals {
  storage_account_name = "${var.env}-${var.storage_account_name}"
  container_name       = "${var.env}-${var.container_name}"
}

resource "azurerm_storage_account" "storage_account_name" {
  name                     = local.storage_account_name
  resource_group_name      = var.resource_group_name
  location                 = var.resource_group_location
  account_tier             = "Standard" # Standard or  Premium
  account_kind             = "StorageV2"   
        # {Storage, StorageV2, BlobStorage}, {BlobStorage, BlockBlobStorage, FileStorage}

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
  name                  = local.container_name 
  storage_account_id    = azurerm_storage_account.storage.id                
  container_access_type = "private"
}
