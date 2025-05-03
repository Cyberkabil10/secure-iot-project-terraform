# This role allows Grafana to query Timestream data
resource "aws_iam_role" "grafana_timestream_role" {
  name = "grafana-timestream-access-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "grafana.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# Attach Timestream Permissions to the Role

resource "aws_iam_role_policy" "grafana_timestream_policy" {
  name = "grafana-timestream-policy"
  role = aws_iam_role.grafana_timestream_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "timestream:DescribeEndpoints",
          "timestream:DescribeTable",
          "timestream:ListMeasures",
          "timestream:Select",
          "timestream:SelectValues",
          "timestream:ListDatabases",
          "timestream:ListTables"
        ],
        Resource = "*"
      }
    ]
  })
}


# Associate the IAM Role with the Grafana Workspace

/*resource "aws_grafana_workspace_role_association" "grafana_iam_access" {
  workspace_id = aws_grafana_workspace.secure_iot_grafana.id
  role         = "ADMIN"
  user_type    = "IAM"
  principal_id = aws_iam_role.grafana_timestream_role.arn
}*/
/*resource "aws_grafana_role_association" "sso_admin_access" {
  workspace_id = aws_grafana_workspace.secure_iot_grafana.id
  role         = "ADMIN"
  group_ids    = ["YOUR_SSO_GROUP_ID"]  # Or use `user_ids` if assigning to individual users
}*/
