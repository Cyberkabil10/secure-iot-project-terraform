resource "aws_grafana_workspace" "secure_iot_grafana" {
  name                     = "secure-iot-grafana"
  account_access_type      = "CURRENT_ACCOUNT"
  authentication_providers = ["AWS_SSO"]
  permission_type          = "SERVICE_MANAGED"
  data_sources             = ["TIMESTREAM"]
  role_arn                 = aws_iam_role.grafana_timestream_role.arn
}
