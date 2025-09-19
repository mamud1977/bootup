resource "azurerm_eventgrid_event_subscription" "blob_created" {
  name  = var.subscription_name
  scope = var.storage_account_id
  included_event_types = ["Microsoft.Storage.BlobCreated"]
  event_delivery_schema = "EventGridSchema"

  advanced_filter {
    key          = "subject"
    operator_type = "StringEndsWith"
    values       = [".txt", ".parquet"]
  }

  azure_function_endpoint {
    function_id = "${var.function_app_id}/functions/${var.function_name}"
  }

  labels = var.labels
  tags   = var.tags

}

