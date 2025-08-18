terraform {
  required_providers {
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~> 0.79.0"
    }
  }
}

provider "snowflake" {
  account = var.snowflake_account
  role    = var.snowflake_role
}

resource "snowflake_database" "demo_db" {
  name    = var.database_name
  comment = "Terraform-managed database"
}

resource "snowflake_warehouse" "demo_wh" {
  name           = var.warehouse_name
  warehouse_size = "XSMALL"
  auto_suspend   = 300
  comment        = "Terraform-managed warehouse"
}

resource "snowflake_role" "demo_role" {
  name    = var.role_name
  comment = "Custom role managed by Terraform"
}

resource "snowflake_user" "demo_user" {
  name         = var.user_name
  password     = var.user_password
  default_role = snowflake_role.demo_role.name
  comment      = "User managed by Terraform"
}

resource "snowflake_role_grants" "assign_role_to_user" {
  role_name = snowflake_role.demo_role.name
  users     = [snowflake_user.demo_user.name]
}

