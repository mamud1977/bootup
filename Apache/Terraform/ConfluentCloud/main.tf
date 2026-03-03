terraform {
  required_providers {
    confluent = {
      source  = "confluentinc/confluent"
      version = "~> 2.0"
    }
  }
}

provider "confluent" {
  cloud_api_key    = var.confluent_api_key
  cloud_api_secret = var.confluent_api_secret
}

############################
# ENVIRONMENT
############################

resource "confluent_environment" "env" {
  display_name = var.environment_name
}

############################
# KAFKA CLUSTER
############################

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

############################
# SERVICE ACCOUNT
############################

resource "confluent_service_account" "sa" {
  display_name = "${var.environment_name}-sa"
}

############################
# RBAC (Topic Level Manage)
############################

resource "confluent_role_binding" "topic_manager" {
  principal = "User:${confluent_service_account.sa.id}"
  role_name = "DeveloperManage"

  crn_pattern = "${confluent_kafka_cluster.cluster.rbac_crn}/kafka=${confluent_kafka_cluster.cluster.id}/topic=*"
}

############################
# KAFKA API KEY
############################

resource "confluent_api_key" "kafka_cluster_key" {
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

############################
# KAFKA TOPIC
############################

resource "confluent_kafka_topic" "topic" {
  topic_name       = var.topic_name
  partitions_count = var.topic_partitions

  config = {
    "cleanup.policy" = "delete"
    "retention.ms"   = var.topic_retention_ms
  }

  kafka_cluster {
    id = confluent_kafka_cluster.cluster.id
  }

  rest_endpoint = confluent_kafka_cluster.cluster.rest_endpoint

  credentials {
    key    = confluent_api_key.kafka_cluster_key.id
    secret = confluent_api_key.kafka_cluster_key.secret
  }

  depends_on = [
    confluent_role_binding.topic_manager,
    confluent_api_key.kafka_cluster_key
  ]
}

############################
# FLINK COMPUTE POOL
############################

resource "confluent_flink_compute_pool" "compute_pool" {
  display_name = var.flink_compute_pool_name
  cloud        = var.cloud
  region       = var.region
  max_cfu      = var.max_cfu

  environment {
    id = confluent_environment.env.id
  }
}

############################
# OUTPUTS
############################

output "environment_id" {
  value = confluent_environment.env.id
}

output "cluster_id" {
  value = confluent_kafka_cluster.cluster.id
}

output "bootstrap_endpoint" {
  value = confluent_kafka_cluster.cluster.bootstrap_endpoint
}

output "rest_endpoint" {
  value = confluent_kafka_cluster.cluster.rest_endpoint
}

output "topic_name" {
  value = confluent_kafka_topic.topic.topic_name
}

output "flink_compute_pool_id" {
  value = confluent_flink_compute_pool.compute_pool.id
}