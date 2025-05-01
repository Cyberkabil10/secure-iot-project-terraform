resource "aws_timestreamwrite_database" "iot_db" {
  database_name = "secure_iot_db"
}

resource "aws_timestreamwrite_table" "iot_table" {
  database_name = aws_timestreamwrite_database.iot_db.database_name
  table_name    = "system_metrics"

  retention_properties {
    memory_store_retention_period_in_hours = 24
    magnetic_store_retention_period_in_days = 7
  }
}

