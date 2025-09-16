output "function_app_hostname" {
  value = "https://${azurerm_linux_function_app.function_app.default_hostname}"
}

