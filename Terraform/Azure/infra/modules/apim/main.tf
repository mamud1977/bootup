# modules/apim/main.tf

####### Create an APIM

resource "azurerm_api_management" "apim" {
  name                = var.apim_name

  location            = var.resource_group_location
  resource_group_name = var.resource_group_name
  
  publisher_name      = var.publisher_name
  publisher_email     = var.publisher_email
  sku_name            = var.sku_name

  identity {
    type = "SystemAssigned"
  }

  tags = var.tags
}


####### Create an API

resource "azurerm_api_management_api" "function_api" {
  name                = "func-api-${var.env}"
  resource_group_name = var.resource_group_name
  api_management_name = azurerm_api_management.apim.name
  revision            = "1"
  display_name        = "HTTP Function API"
  path                = "function"
  protocols           = ["https"]
}

####### Define operation

resource "azurerm_api_management_api_operation" "match_po" {
  operation_id        = "match-po"
  api_name            = azurerm_api_management_api.function_api.name
  api_management_name = azurerm_api_management.apim.name
  resource_group_name = var.resource_group_name
  display_name        = "Match PO Number"
  method              = "GET"
  url_template        = "/match"
  response {
    status_code = 200
    description = "Successful match"
  }
}

###### Wire the Backend

resource "azurerm_api_management_api_operation_policy" "match_po_policy" {
  operation_id        = azurerm_api_management_api_operation.match_po.operation_id
  api_name            = azurerm_api_management_api.function_api.name
  api_management_name = azurerm_api_management.apim.name
  resource_group_name = var.resource_group_name

  xml_content = <<XML
  <policies>
  <inbound>
    <base />
    <set-backend-service base-url="https://${var.function_app_hostname}/api/match-po" />
  </inbound>
  <backend>
    <base />
  </backend>
  <outbound>
    <base />
  </outbound>
  </policies>
  XML
}

