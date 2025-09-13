# storage module -> main.tf

resource "azurerm_storage_account" "storage_account" {
  name                     = var.storage_account_name
  resource_group_name      = var.resource_group_name
  location                 = var.resource_group_location
  
  account_tier             = "Standard"  # Standard or  Premium
  account_kind             = "StorageV2" # {Storage, StorageV2, BlobStorage}, {BlobStorage, BlockBlobStorage, FileStorage}
  account_replication_type = "LRS"
  
  access_tier              = "Hot"

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

resource "azurerm_storage_management_policy" "cool_and_delete_snapshots" {
  storage_account_id = azurerm_storage_account.storage_account.id

  rule {
    name    = "cool-after-45-days-delete-snapshots"
    enabled = true

    filters {
      blob_types   = ["blockBlob"]
      prefix_match = [""] # Empty string = all blobs
    }

    actions {
      base_blob {
        tier_to_cool {
          days_since_last_access_time_greater_than = 45
        }

        delete {
          days_after_creation_greater_than = 365 # Optional: delete base blob after 1 year
        }
      }

      snapshot {
        delete {
          days_after_creation_greater_than = 0 # Delete all snapshots immediately
        }
      }
    }
  }
}


resource "azurerm_storage_container" "my_container" {
  name                    = var.container_name 
  storage_account_name    = azurerm_storage_account.storage_account.name               
  container_access_type   = "private"
}

