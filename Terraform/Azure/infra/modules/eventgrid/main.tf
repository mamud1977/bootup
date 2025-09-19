resource "azurerm_eventgrid_event_subscription" "eventgrid_triggerd" {
  name  = var.subscription_name
  scope = var.storage_account_id
  included_event_types = [
    "Microsoft.Storage.BlobCreated",
    "Microsoft.Storage.BlobDeleted"
    ]
  
  event_delivery_schema = "EventGridSchema"


  azure_function_endpoint {
    function_id = "${var.function_app_id}/functions/${var.function_name_eventgrid_triggered}"
  }

  labels = var.labels

}

