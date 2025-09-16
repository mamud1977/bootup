# modules/apim/main.tf

########### 1. Create an APIM

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


########### 2. Creating the APIM API resource

resource "azurerm_api_management_api" "function_api" {
  name                = "hhtp-triggered-function-api-${var.env}"
  resource_group_name = var.resource_group_name
  api_management_name = azurerm_api_management.apim.name
  revision            = "1"
  display_name        = "HTTP Function API - Best PO Number mathing"
  path                = "best-po-number-matching"
  protocols           = ["https"]
}

########### Define operation

