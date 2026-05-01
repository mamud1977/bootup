############################################
# data layer : main.tf
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

  kafka_api_key       = data.terraform_remote_state.infra.outputs.kafka_api_key
  kafka_api_secret    = data.terraform_remote_state.infra.outputs.kafka_api_secret
  kafka_rest_endpoint = data.terraform_remote_state.infra.outputs.kafka_rest_endpoint
}

data "terraform_remote_state" "infra" {
  backend = "local"

  config = {
    path = "../infra-layer/terraform.tfstate"
  }
}

############################################
# KAFKA TOPICS
############################################

############# 1:1 topic

resource "confluent_kafka_topic" "topic-orders" {
  topic_name       = "topic-orders"
  partitions_count = 3

  config = {
    "cleanup.policy" = "delete"
    "retention.ms"   = 604800000
  }

  kafka_cluster {
    id = data.terraform_remote_state.infra.outputs.cluster_id
  }
}

############# M:1 topic

resource "confluent_kafka_topic" "topic-multi-1" {
  topic_name       = "topic-multi-1"
  partitions_count = 3

  config = {
    "cleanup.policy" = "delete"
    "retention.ms"   = 604800000
  }

  kafka_cluster {
    id = data.terraform_remote_state.infra.outputs.cluster_id
  }
}

############# Linking Multiple Schemas

resource "confluent_schema" "orders" {
  schema_registry_cluster {
    id = data.terraform_remote_state.infra.outputs.schema_registry_id 
  }
  
  rest_endpoint = data.terraform_remote_state.infra.outputs.schema_registry_endpoint

  # The subject name for the orders topic
  # subject_name  = "com.testdb.orders"
  subject_name = "${confluent_kafka_topic.topic-multi-1.topic_name}-com.testdb.orders"
  format       = "AVRO"
  
  # Points to your local file: schemas/create_order.avsc
  schema = file("./schemas/orders.avsc")

  credentials {
    key    = data.terraform_remote_state.infra.outputs.schema_registry_api_key
    secret = data.terraform_remote_state.infra.outputs.schema_registry_api_secret
  }

}

resource "confluent_schema" "events" {
  schema_registry_cluster {
    id = data.terraform_remote_state.infra.outputs.schema_registry_id 
  }
  
  rest_endpoint = data.terraform_remote_state.infra.outputs.schema_registry_endpoint

  # The subject name for the orders topic
  # subject_name  = "com.testdb.events"
  subject_name = "${confluent_kafka_topic.topic-multi-1.topic_name}-com.testdb.events"
  format       = "AVRO"
  
  schema = file("./schemas/events.avsc")

  credentials {
    key    = data.terraform_remote_state.infra.outputs.schema_registry_api_key
    secret = data.terraform_remote_state.infra.outputs.schema_registry_api_secret
  }

}


############################################
# SNOWFLAKE SOURCE CONNECTOR
############################################

resource "confluent_connector" "snowflake_source" {

  environment {
    id = data.terraform_remote_state.infra.outputs.environment_id
  }

  kafka_cluster {
    id = data.terraform_remote_state.infra.outputs.cluster_id
  }

  config_nonsensitive = {

    "name"                    = "snowflake-source"
    "connector.class"         = "SnowflakeSource"

    "connection.url"          = var.snowflake_url
    "connection.user"         = var.snowflake_user

    "table.include.list" = "TESTDB.TESTSCHEMA1.EVENTS, TESTDB.TESTSCHEMA1.ORDERS"
    
    #"mode"                    = "timestamp"
    #"timestamp.columns.mapping" = "TESTDB.TESTSCHEMA1.EVENTS:[UPDATED_AT]"


    # for SINGLE_ZONE table mapping
    #"mode" = "timestamp+incrementing"
    #"timestamp.column.name" = "UPDATED_AT"
    #"incrementing.column.name" = "ID"


    # for multi table mapping
    "mode"                        = "timestamp+incrementing" 
    "timestamp.columns.mapping"   = ".*:[UPDATED_AT]"
    "incrementing.column.mapping" = ".*:ID"
    
 
    "topic.prefix"            = "snowflake-"
    "db.timezone"             = "UTC"

    "tasks.max"               = "1"
    "poll.interval.ms"        = "1000"
    "timestamp.granularity"   = "NANOS_LONG"
    "table.types"             = "TABLE"
    "output.data.format"      = "AVRO"

    "value.converter" = "io.confluent.connect.avro.AvroConverter"
    "value.converter.schema.registry.url" = data.terraform_remote_state.infra.outputs.schema_registry_endpoint
    "value.converter.basic.auth.credentials.source" = "USER_INFO"
    "value.converter.basic.auth.user.info" = "${data.terraform_remote_state.infra.outputs.schema_registry_api_key}:${data.terraform_remote_state.infra.outputs.schema_registry_api_secret}"

  # Topic auto-creation settings
    "topic.creation.default.replication.factor" = "3"
    "topic.creation.default.partitions"         = "3"
    "topic.creation.default.retention.ms"       = "3600000"
  }

  config_sensitive = {
    "connection.private.key" = var.snowflake_private_key
    "kafka.api.key"          = data.terraform_remote_state.infra.outputs.kafka_api_key
    "kafka.api.secret"       = data.terraform_remote_state.infra.outputs.kafka_api_secret
  }
}

