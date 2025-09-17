resource "azurerm_eventgrid_event_subscription" "blob_created_trigger" {
  name  = var.subscription_name
  scope = var.storage_account_id

  event_delivery_schema = "EventGridSchema"
  included_event_types  = ["Microsoft.Storage.BlobCreated"]

  azure_function_endpoint {
    function_id = var.function_app_id
  }

  advanced_filter {
    string_ends_with {
      key    = "data.url"
      values = [".parquet"]
    }
  }
  
  retry_policy {
    max_delivery_attempts = 5
    event_time_to_live    = 1440
  }

  labels = var.labels

}

