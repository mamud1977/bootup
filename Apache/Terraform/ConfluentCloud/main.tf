############################################
# TERRAFORM CONFIGURATION
############################################

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
}

############################################
# ENVIRONMENT
############################################

resource "confluent_environment" "env" {
  display_name = var.environment_name
}

############################################
# KAFKA CLUSTER
############################################

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

############################################
# SERVICE ACCOUNTS
############################################

resource "confluent_service_account" "sa" {
  display_name = "${var.environment_name}-sa"
}

resource "confluent_service_account" "cluster_admin_sa" {
  display_name = "${var.environment_name}-cluster-admin-sa"
}

############################################
# ROLE BINDINGS (RBAC)
############################################

resource "confluent_role_binding" "cluster_admin_binding" {
  principal   = "User:${confluent_service_account.cluster_admin_sa.id}"
  role_name   = "CloudClusterAdmin"
  crn_pattern = confluent_kafka_cluster.cluster.rbac_crn
}

resource "confluent_role_binding" "topic_manager" {
  principal = "User:${confluent_service_account.sa.id}"
  role_name = "DeveloperManage"

  crn_pattern = "${confluent_kafka_cluster.cluster.rbac_crn}/kafka=${confluent_kafka_cluster.cluster.id}/topic=*"
}

resource "confluent_role_binding" "cluster_writer" {
  principal   = "User:${confluent_service_account.sa.id}"
  role_name   = "DeveloperWrite"
  crn_pattern = "${confluent_kafka_cluster.cluster.rbac_crn}/kafka=${confluent_kafka_cluster.cluster.id}"
}

############################################
# API KEYS
############################################

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

resource "confluent_api_key" "kafka_cluster_admin" {
  display_name = "${var.environment_name}-cluster-admin-key"

  owner {
    id          = confluent_service_account.cluster_admin_sa.id
    api_version = confluent_service_account.cluster_admin_sa.api_version
    kind        = confluent_service_account.cluster_admin_sa.kind
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

############################################
# KAFKA TOPIC
############################################

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
    confluent_role_binding.topic_manager
  ]
}

############################################
# SCHEMA REGISTRY
############################################

data "confluent_schema_registry_cluster" "sr" {
  environment {
    id = confluent_environment.env.id
  }

  depends_on = [
    confluent_kafka_cluster.cluster
  ]
}

resource "confluent_api_key" "schema_registry_key" {
  display_name = "schema-registry-api-key"

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
# FLINK COMPUTE POOL
############################################

resource "confluent_flink_compute_pool" "compute_pool" {
  display_name = var.flink_compute_pool_name
  cloud        = var.cloud
  region       = var.region
  max_cfu      = var.max_cfu

  environment {
    id = confluent_environment.env.id
  }
}

############################################
# SNOWFLAKE SOURCE CONNECTOR
############################################

resource "confluent_connector" "snowflake_source" {

  environment {
    id = confluent_environment.env.id
  }

  kafka_cluster {
    id = confluent_kafka_cluster.cluster.id
  }

  config_nonsensitive = {

    "name"                    = "snowflake-source"
    "connector.class"         = "SnowflakeSource"

    "connection.url"          = var.snowflake_url
    "connection.user"         = var.snowflake_user

    "table.include.list"      = "TESTDB.TESTSCHEMA1.EVENTS"
    
    "mode"                    = "timestamp"
    "timestamp.columns.mapping" = "TESTDB.TESTSCHEMA1.EVENTS:[UPDATED_AT]"


    # for SINGLE_ZONE table mapping
    #"mode" = "timestamp+incrementing"
    #"timestamp.column.name" = "UPDATED_AT"
    #"incrementing.column.name" = "EVENT_ID"


    # for multi table mapping
    #"mode" = "timestamp+incrementing"
    #"timestamp.columns.mapping" = "TESTDB.TESTSCHEMA1.EVENTS:[UPDATED_AT]"
    #"incrementing.columns.mapping" = "TESTDB.TESTSCHEMA1.EVENTS:[EVENT_ID]"
 

    "topic.prefix"            = "snowflake-"
    "db.timezone"             = "UTC"

    "tasks.max"               = "1"
    "poll.interval.ms"        = "1000"
    "timestamp.granularity"   = "NANOS_LONG"
    "table.types"             = "TABLE"
    "output.data.format"      = "AVRO"

    "value.converter" = "io.confluent.connect.avro.AvroConverter"
    "value.converter.schema.registry.url" = data.confluent_schema_registry_cluster.sr.rest_endpoint
    "value.converter.basic.auth.credentials.source" = "USER_INFO"
    "value.converter.basic.auth.user.info" = "${confluent_api_key.schema_registry_key.id}:${confluent_api_key.schema_registry_key.secret}"

  # Topic auto-creation settings
    "topic.creation.default.replication.factor" = "2"
    "topic.creation.default.partitions"         = "2"
    "topic.creation.default.retention.ms"       = "3600000"

  }

  config_sensitive = {
    "connection.private.key" = var.snowflake_private_key
    "kafka.api.key"          = confluent_api_key.kafka_cluster_key.id
    "kafka.api.secret"       = confluent_api_key.kafka_cluster_key.secret
  }
}



############################################
# Kafka AWS S3 Sink Connector
############################################

resource "confluent_connector" "s3_sink" {

  environment {
    id = confluent_environment.env.id
  }

  kafka_cluster {
    id = confluent_kafka_cluster.cluster.id
  }

  lifecycle {
  create_before_destroy = true
  }


  config_nonsensitive = {

    "name" = "s3-sink"

    "connector.class" = "S3_SINK"

    "topics.regex" = "snowflake-TESTDB.TESTSCHEMA1.EVENTS"

    "s3.bucket.name" = "my-kafka-s3-bucket-1234512345"
    "s3.region"      = var.region

    "aws.access.key.id" = var.aws_access_key

    "flush.size" = "1000"
    "tasks.max"  = "1"

    # Output format
    "format.class" = "io.confluent.connect.s3.format.avro.AvroFormat"
    "input.data.format"  = "AVRO"
    "output.data.format" = "AVRO"


    # Avro converters
    "key.converter"   = "io.confluent.connect.avro.AvroConverter"
    "value.converter" = "io.confluent.connect.avro.AvroConverter"

    "key.converter.schema.registry.url"   = data.confluent_schema_registry_cluster.sr.rest_endpoint
    "value.converter.schema.registry.url" = data.confluent_schema_registry_cluster.sr.rest_endpoint

    "key.converter.basic.auth.credentials.source" = "USER_INFO"
    "value.converter.basic.auth.credentials.source" = "USER_INFO"

    "key.converter.basic.auth.user.info" = "${confluent_api_key.schema_registry_key.id}:${confluent_api_key.schema_registry_key.secret}"
    "value.converter.basic.auth.user.info" = "${confluent_api_key.schema_registry_key.id}:${confluent_api_key.schema_registry_key.secret}"

    "locale"   = "en-US"
    "timezone" = "UTC"

    "time.interval" = "DAILY"

    # DLQ
    "errors.tolerance"                         = "all"
    "errors.deadletterqueue.topic.name"        = "dlq-s3-sink"
    "errors.deadletterqueue.context.headers.enable" = "true"

    "kafka.auth.mode"          = "KAFKA_API_KEY"
    "kafka.service.account.id" = confluent_service_account.sa.id
  }

  config_sensitive = {

    "aws.secret.access.key" = var.aws_secret_access_key

    "kafka.api.key"    = confluent_api_key.kafka_cluster_key.id
    "kafka.api.secret" = confluent_api_key.kafka_cluster_key.secret
  }


  depends_on = [
    confluent_kafka_cluster.cluster
  ]
}

############################################
# SF CONNECTOR ACLs
############################################

resource "confluent_kafka_acl" "snowflake_connector_describe_cluster" {
  kafka_cluster { id = confluent_kafka_cluster.cluster.id }

  resource_type = "CLUSTER"
  resource_name = "kafka-cluster"
  pattern_type  = "LITERAL"
  principal     = "User:${confluent_service_account.sa.id}"
  host          = "*"
  operation     = "DESCRIBE"
  permission    = "ALLOW"

  rest_endpoint = confluent_kafka_cluster.cluster.rest_endpoint

  credentials {
    key    = confluent_api_key.kafka_cluster_admin.id
    secret = confluent_api_key.kafka_cluster_admin.secret
  }
}

resource "confluent_kafka_acl" "snowflake_connector_create_prefix" {
  kafka_cluster { id = confluent_kafka_cluster.cluster.id }

  resource_type = "TOPIC"
  resource_name = "snowflake-"
  pattern_type  = "PREFIXED"
  principal     = "User:${confluent_service_account.sa.id}"
  host          = "*"
  operation     = "CREATE"
  permission    = "ALLOW"

  rest_endpoint = confluent_kafka_cluster.cluster.rest_endpoint

  credentials {
    key    = confluent_api_key.kafka_cluster_admin.id
    secret = confluent_api_key.kafka_cluster_admin.secret
  }
}

resource "confluent_kafka_acl" "snowflake_connector_write_prefix" {
  kafka_cluster { id = confluent_kafka_cluster.cluster.id }

  resource_type = "TOPIC"
  resource_name = "snowflake-"
  pattern_type  = "PREFIXED"
  principal     = "User:${confluent_service_account.sa.id}"
  host          = "*"
  operation     = "WRITE"
  permission    = "ALLOW"

  rest_endpoint = confluent_kafka_cluster.cluster.rest_endpoint

  credentials {
    key    = confluent_api_key.kafka_cluster_admin.id
    secret = confluent_api_key.kafka_cluster_admin.secret
  }
}


############################################
# AWS S3 CONNECTOR ACLs
############################################

# Topic Permissions
resource "confluent_kafka_acl" "s3_sink_topic_read" {

  kafka_cluster {
    id = confluent_kafka_cluster.cluster.id
  }

  rest_endpoint = confluent_kafka_cluster.cluster.rest_endpoint

  credentials {
    key    = confluent_api_key.kafka_cluster_admin.id
    secret = confluent_api_key.kafka_cluster_admin.secret
  }

  resource_type = "TOPIC"
  resource_name = "snowflake-"
  pattern_type  = "PREFIXED"

  principal = "User:${confluent_service_account.sa.id}"

  host = "*"

  operation  = "READ"
  permission = "ALLOW"
}

# Consumer Group Permissions
resource "confluent_kafka_acl" "s3_sink_group_read" {

  kafka_cluster {
    id = confluent_kafka_cluster.cluster.id
  }

  rest_endpoint = confluent_kafka_cluster.cluster.rest_endpoint

  credentials {
    key    = confluent_api_key.kafka_cluster_admin.id
    secret = confluent_api_key.kafka_cluster_admin.secret
  }

  resource_type = "GROUP"
  resource_name = "connect-lcc-"
  pattern_type  = "PREFIXED"

  principal = "User:${confluent_service_account.sa.id}"

  host = "*"

  operation  = "READ"
  permission = "ALLOW"
}


# DESCRIBE and DELETE (Confluent requires them for connectors).

resource "confluent_kafka_acl" "s3_sink_group_describe" {

  kafka_cluster {
    id = confluent_kafka_cluster.cluster.id
  }

  rest_endpoint = confluent_kafka_cluster.cluster.rest_endpoint

  credentials {
    key    = confluent_api_key.kafka_cluster_admin.id
    secret = confluent_api_key.kafka_cluster_admin.secret
  }

  resource_type = "GROUP"
  resource_name = "connect-lcc-"
  pattern_type  = "PREFIXED"

  principal = "User:${confluent_service_account.sa.id}"

  host = "*"

  operation  = "DESCRIBE"
  permission = "ALLOW"
}

resource "confluent_kafka_acl" "s3_sink_group_delete" {

  kafka_cluster {
    id = confluent_kafka_cluster.cluster.id
  }

  rest_endpoint = confluent_kafka_cluster.cluster.rest_endpoint

  credentials {
    key    = confluent_api_key.kafka_cluster_admin.id
    secret = confluent_api_key.kafka_cluster_admin.secret
  }

  resource_type = "GROUP"
  resource_name = "connect-lcc-"
  pattern_type  = "PREFIXED"

  principal = "User:${confluent_service_account.sa.id}"

  host = "*"

  operation  = "DELETE"
  permission = "ALLOW"
}

############################################
# ACL for DLQ Topics
############################################
resource "confluent_kafka_acl" "dlq_write" {
  kafka_cluster {
    id = confluent_kafka_cluster.cluster.id
  }

  resource_type = "TOPIC"
  resource_name = "dlq-"
  pattern_type  = "PREFIXED"

  principal   = "User:${confluent_service_account.sa.id}"
  host        = "*"
  operation   = "WRITE"
  permission  = "ALLOW"

  rest_endpoint = confluent_kafka_cluster.cluster.rest_endpoint

  credentials {
    key    = confluent_api_key.kafka_cluster_admin.id
    secret = confluent_api_key.kafka_cluster_admin.secret
  }
}

resource "confluent_kafka_acl" "dlq_read" {
  kafka_cluster {
    id = confluent_kafka_cluster.cluster.id
  }

  resource_type = "TOPIC"
  resource_name = "dlq-"
  pattern_type  = "PREFIXED"

  principal   = "User:${confluent_service_account.sa.id}"
  host        = "*"
  operation   = "READ"
  permission  = "ALLOW"

  rest_endpoint = confluent_kafka_cluster.cluster.rest_endpoint

  credentials {
    key    = confluent_api_key.kafka_cluster_admin.id
    secret = confluent_api_key.kafka_cluster_admin.secret
  }
}

resource "confluent_kafka_acl" "dlq_describe" {
  kafka_cluster {
    id = confluent_kafka_cluster.cluster.id
  }

  resource_type = "TOPIC"
  resource_name = "dlq-"
  pattern_type  = "PREFIXED"

  principal   = "User:${confluent_service_account.sa.id}"
  host        = "*"
  operation   = "DESCRIBE"
  permission  = "ALLOW"

  rest_endpoint = confluent_kafka_cluster.cluster.rest_endpoint

  credentials {
    key    = confluent_api_key.kafka_cluster_admin.id
    secret = confluent_api_key.kafka_cluster_admin.secret
  }
}



############################################
# OUTPUTS
############################################

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

output "schema_registry_endpoint" {
  value = data.confluent_schema_registry_cluster.sr.rest_endpoint
}

output "schema_registry_api_key" {
  value     = confluent_api_key.schema_registry_key.id
  sensitive = true
}

output "schema_registry_api_secret" {
  value     = confluent_api_key.schema_registry_key.secret
  sensitive = true
}