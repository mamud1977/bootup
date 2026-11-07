############################################
# infra : terraform.tfvars
############################################

# Confluent Cloud credentials (sensitive)
confluent_api_key    = "TVHR3DBHUIFP7Y2J"
confluent_api_secret = "cfltVJFNvJUcWuBziUZ0S8U5ysQvoh/bhTqzz9M/S2XLL+VJ9WYmlsazkKN3Y9tA"

# Environment & Kafka cluster
environment_name = "dev"
cluster_name     = "dev-cluster"
cloud            = "AWS"
region           = "us-east-1"

# Flink compute pool
flink_compute_pool_name = "my-flink-pool"
max_cfu                 = 5