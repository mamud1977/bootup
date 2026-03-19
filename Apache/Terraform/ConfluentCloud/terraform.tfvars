confluent_api_key    = <>
confluent_api_secret = <>

environment_name = "terraform-env"
cluster_name     = "terraform-cluster"
region           = "us-east-1"
cloud            = "AWS"

topic_name       = "orders-topic"
topic_partitions = 3

flink_compute_pool_name = "sql-course"
max_cfu                 = 5