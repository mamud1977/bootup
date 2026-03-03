#####  modules/apim/main.tf

##########  1. Create an Azure function App

##########  2. Deploy one or many funtions

##########  3. Create an APIM

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


##########  4. Creating the APIM API resource

resource "azurerm_api_management_api" "function_api" {
  name                = "hhtp-triggered-function-api-${var.env}"
  resource_group_name = var.resource_group_name
  api_management_name = azurerm_api_management.apim.name
  revision            = "1"
  display_name        = "HTTP Function API - Best PO Number mathing"
  path                = "best-po-number-matching"
  protocols           = ["https"]
}

##########  5. Define the Operation

resource "azurerm_api_management_api_operation" "http_triggered" {
  operation_id        = "http-triggered"
  api_name            = azurerm_api_management_api.function_api.name
  api_management_name = azurerm_api_management.apim.name
  resource_group_name = var.resource_group_name

  display_name        = "HTTP Triggered Function"
  method              = "GET"
  url_template        = "/http-triggered"

  request {
    query_parameter {
      name     = "po_number"
      required = false
      type     = "string"
    }
  }

  response {
    status_code = 200
    description = "Function executed successfully"
  }
}


########## 6.Route to Azure Function Backend

resource "azurerm_api_management_named_value" "function_key" {
  name                = "function-key"
  display_name        = "Function Key"
  value               = var.function_key
  secret              = true
  api_management_name = azurerm_api_management.apim.name
  resource_group_name = var.resource_group_name
}


resource "azurerm_api_management_api_operation_policy" "http_triggered_policy" {
  operation_id        = azurerm_api_management_api_operation.http_triggered.operation_id
  api_name            = azurerm_api_management_api.function_api.name
  api_management_name = azurerm_api_management.apim.name
  resource_group_name = var.resource_group_name

  xml_content = <<XML
<policies>
  <inbound>
    <base />
    <set-header name="x-functions-key" exists-action="override">
      <value>{{function_key}}</value>
    </set-header>
    <rate-limit calls="100" renewal-period="60" />
    <set-backend-service base-url="https://function-app-dev-ijfviz.azurewebsites.net/api/http-triggered" />
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


########## 7. Create an APIM Product - a logical container for one or more APIs, with access rules

resource "azurerm_api_management_product" "po_matcher_product" {
  product_id            = "po-matcher-product"
  api_management_name   = azurerm_api_management.apim.name
  resource_group_name   = var.resource_group_name

  display_name          = "PO Matcher Product"
  description           = "Secure access to PO matching API"
  subscription_required = true  # Enforces access control: users must have a valid subscription key to call APIs in this product.
  approval_required     = false # Users can self-subscribe without manual approval.
  published             = true  # Makes the product visible in the developer portal.
  subscriptions_limit   = 5     # Limits the number of subscriptions a user can create for this product.
}

########## 8. Link Your API to the Product

resource "azurerm_api_management_product_api" "po_matcher_link" {
  api_name            = azurerm_api_management_api.function_api.name
  product_id          = azurerm_api_management_product.po_matcher_product.product_id
  api_management_name = azurerm_api_management.apim.name
  resource_group_name = var.resource_group_name
}
