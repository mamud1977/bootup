resource "azurerm_eventgrid_event_subscription" "event_subscription" {
  name  = var.subscription_name
  scope = var.storage_account_id
  included_event_types = [
    "Microsoft.Storage.BlobCreated",
    "Microsoft.Storage.BlobDeleted"
  ]

  # Filter events for a specific container
  subject_filter {
    subject_begins_with = "/blobServices/default/containers/parquet-files/blobs/"
  }  

  event_delivery_schema = "EventGridSchema"

  azure_function_endpoint {
    function_id = "${var.function_app_id}/functions/${var.function_name_eventgrid_triggered}"
  }


  # Dead-lettering configuration
  dead_letter_destination {
    storage_blob {
      resource_id       = var.storage_account_id
      container_name    = azurerm_storage_container.dead_letter_container.name
    }
  }


  labels = var.labels

}

