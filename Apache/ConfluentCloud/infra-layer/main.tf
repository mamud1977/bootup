###########################################################
# infra: main.tf
###########################################################

terraform {
  required_providers {
    confluent = {
      source  = "confluentinc/confluent"
      version = "~> 2.60"
    }
  }
}

provider "confluent" {
  cloud_api_key    = var.confluent_api_key
  cloud_api_secret = var.confluent_api_secret

  # Explicitly unset Kafka credentials to satisfy Terraform
  kafka_api_key       = null
  kafka_api_secret    = null
  kafka_rest_endpoint = null
}

###########################################################
# ENVIRONMENT
###########################################################

resource "confluent_environment" "env" {
  display_name = var.environment_name
}


###########################################################
# KAFKA CLUSTER
###########################################################

resource "confluent_kafka_cluster" "cluster" {
  display_name = var.cluster_name
  availability = "SINGLE_ZONE"
  cloud        = var.cloud
  region       = var.region

  standard {}

  environment {
    id = confluent_environment.env.id
  }

  lifecycle {
    prevent_destroy = false
  }
}

###########################################################
# FLINK COMPUTE POOL
###########################################################

resource "confluent_flink_compute_pool" "compute_pool" {
  display_name = var.flink_compute_pool_name
  cloud        = var.cloud
  region       = var.region
  max_cfu      = var.max_cfu

  environment {
    id = confluent_environment.env.id
  }
}


###########################################################
# SERVICE ACCOUNTS
###########################################################

resource "confluent_service_account" "sa" {
  display_name = "${var.environment_name}-sa"
}

###########################################################
# SERVICE ACCOUNTS - API KEYS
###########################################################

resource "confluent_api_key" "kafka_cluster_key_sa" {
  display_name = "${var.environment_name}-kafka-key"

  owner {
    id          = confluent_service_account.sa.id
    api_version = confluent_service_account.sa.api_version
    kind        = confluent_service_account.sa.kind
  }

  managed_resource {
    id          = confluent_kafka_cluster.cluster.id
    api_version = confluent_kafka_cluster.cluster.api_version
    kind        = confluent_kafka_cluster.cluster.kind

    environment {
      id = confluent_environment.env.id
    }
  }
}

###########################################################
# SERVICE ACCOUNTS - ROLE BINDINGS
###########################################################

resource "confluent_role_binding" "cluster_writer" {
  principal   = "User:${confluent_service_account.sa.id}"
  role_name   = "DeveloperWrite"
  crn_pattern = "${confluent_kafka_cluster.cluster.rbac_crn}/kafka=${confluent_kafka_cluster.cluster.id}"
}

resource "confluent_role_binding" "topic_manager" {
  principal = "User:${confluent_service_account.sa.id}"
  role_name = "DeveloperManage"
  crn_pattern = "${confluent_kafka_cluster.cluster.rbac_crn}/kafka=${confluent_kafka_cluster.cluster.id}/topic=*"
}

resource "confluent_role_binding" "schema_registry_resource_owner" {
  principal   = "User:${confluent_service_account.sa.id}"
  role_name   = "ResourceOwner"
  crn_pattern = "${data.confluent_schema_registry_cluster.sr.resource_name}/subject=*"
}

# Grant the SA permission to manage all snowflake topics
resource "confluent_role_binding" "snowflake_connector_topics" {
  principal   = "User:${confluent_service_account.sa.id}"
  role_name   = "DeveloperManage" # Required for auto-creation
  crn_pattern = "${confluent_kafka_cluster.cluster.rbac_crn}/kafka=${confluent_kafka_cluster.cluster.id}/topic=snowflake-*"
}

resource "confluent_role_binding" "snowflake_connector_write" {
  principal   = "User:${confluent_service_account.sa.id}"
  role_name   = "DeveloperWrite"
  crn_pattern = "${confluent_kafka_cluster.cluster.rbac_crn}/kafka=${confluent_kafka_cluster.cluster.id}/topic=snowflake-*"
}


###########################################################
# SERVICE ACCOUNTS for CLUSTER ADMIN 
###########################################################

resource "confluent_service_account" "sa_cluster_admin" {
  display_name = "${var.environment_name}-sa_cluster_admin"
}

###########################################################
# SERVICE ACCOUNTS for CLUSTER ADMIN - API KEYS
###########################################################

resource "confluent_api_key" "kafka_cluster_key_admin_sa" {
  display_name = "${var.environment_name}-cluster-admin-key"

  owner {
    id          = confluent_service_account.sa_cluster_admin.id
    api_version = confluent_service_account.sa_cluster_admin.api_version
    kind        = confluent_service_account.sa_cluster_admin.kind
  }

  managed_resource {
    id          = confluent_kafka_cluster.cluster.id
    api_version = confluent_kafka_cluster.cluster.api_version
    kind        = confluent_kafka_cluster.cluster.kind

    environment {
      id = confluent_environment.env.id
    }
  }
}

###########################################################
# SERVICE ACCOUNTS for CLUSTER ADMIN - ROLE BINDINGS
###########################################################

resource "confluent_role_binding" "cluster_admin_binding" {
  principal   = "User:${confluent_service_account.sa_cluster_admin.id}"
  role_name   = "CloudClusterAdmin"
  crn_pattern = confluent_kafka_cluster.cluster.rbac_crn
}

###########################################################
# SCHEMA REGISTRY
###########################################################

data "confluent_schema_registry_cluster" "sr" {
  environment {
    id = confluent_environment.env.id
  }

  depends_on = [confluent_environment.env]
}

###########################################################
# SCHEMA REGISTRY - API KEY
###########################################################

resource "confluent_api_key" "sr_key" {
  display_name = "${var.environment_name}-sr-key"

  owner {
    id          = confluent_service_account.sa.id
    api_version = confluent_service_account.sa.api_version
    kind        = confluent_service_account.sa.kind
  }

  managed_resource {
    id          = data.confluent_schema_registry_cluster.sr.id
    api_version = data.confluent_schema_registry_cluster.sr.api_version
    kind        = data.confluent_schema_registry_cluster.sr.kind

    environment {
      id = confluent_environment.env.id
    }
  }
}

############################################
# OUTPUTS
############################################

################ IDs
output "environment_id" {
  value = confluent_environment.env.id
}

output "cluster_id" {
  value = confluent_kafka_cluster.cluster.id
}

output "flink_compute_pool_id" {
  value = confluent_flink_compute_pool.compute_pool.id
}

output "service_account_id" {
  value = confluent_service_account.sa.id
}

output "schema_registry_id" {
  value = data.confluent_schema_registry_cluster.sr.id
}

################ Endpoints

output "bootstrap_endpoint" {
  value = confluent_kafka_cluster.cluster.bootstrap_endpoint
}

output "kafka_rest_endpoint" {
  value = confluent_kafka_cluster.cluster.rest_endpoint
}

output "schema_registry_endpoint" {
  description = "The URL for the Schema Registry"
  value       = data.confluent_schema_registry_cluster.sr.rest_endpoint
}

################ Credentials (Sensitive)
output "kafka_api_key" {
  value     = confluent_api_key.kafka_cluster_key_sa.id
  sensitive = true
}

output "kafka_api_secret" {
  value     = confluent_api_key.kafka_cluster_key_sa.secret
  sensitive = true
}

output "kafka_admin_api_key" {
  value     = confluent_api_key.kafka_cluster_key_admin_sa.id
  sensitive = true
}

output "kafka_admin_api_secret" {
  value     = confluent_api_key.kafka_cluster_key_admin_sa.secret
  sensitive = true
}

output "schema_registry_api_key" {
  description = "SR API Key for the Service Account"
  value       = confluent_api_key.sr_key.id
  sensitive   = true
}

output "schema_registry_api_secret" {
  description = "SR API Secret for the Service Account"
  value       = confluent_api_key.sr_key.secret
  sensitive   = true
}


################ CRNs

output "kafka_cluster_rbac_crn" {
  description = "The RBAC CRN of the Kafka Cluster"
  value       = confluent_kafka_cluster.cluster.rbac_crn
}

