#####  modules/apim/main.tf

#####  1. Create an Azure function App

#####  2. Deploy one or many funtions

#####  3. Create an APIM

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


#####  4. Creating the APIM API resource

resource "azurerm_api_management_api" "function_api" {
  name                = "hhtp-triggered-function-api-${var.env}"
  resource_group_name = var.resource_group_name
  api_management_name = azurerm_api_management.apim.name
  revision            = "1"
  display_name        = "HTTP Function API - Best PO Number mathing"
  path                = "best-po-number-matching"
  protocols           = ["https"]
}

##### 5. Create an APIM Product - a logical container for one or more APIs, with access rules
resource "azurerm_api_management_product" "po_matcher_product" {
  product_id          = "po-matcher-product"
  api_management_name = azurerm_api_management.apim.name
  resource_group_name = var.resource_group_name

  display_name        = "PO Matcher Product"
  description         = "Secure access to PO matching API"
  subscription_required = true  # Enforces access control: users must have a valid subscription key to call APIs in this product.
  approval_required     = false # Users can self-subscribe without manual approval.
  published             = true  # Makes the product visible in the developer portal.
  subscriptions_limit   = 5     # Limits the number of subscriptions a user can create for this product.
}

