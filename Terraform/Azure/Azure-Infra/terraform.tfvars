# terraform.tfvars

env                         = "dev"

tags = {
  environment = "dev"
  owner       = "Mamud"
  project     = "cloud-infra"
}

resource_group_name_1       = "rg"
resource_group_location     = "Central India"

storage_account_name      = "mystorage1"
container_name    = "mycontainer1"

cosmosdb_account_name       = "mycosmosdb1"

