resource "aws_iot_topic_rule" "iot_lambda_rule" {
  name        = "ForwardMetricsToLambda"
  description = "Forwards telemetry to Lambda for Timestream storage"
  enabled     = true
  sql_version = "2016-03-23"

  sql = <<SQL
SELECT * FROM 'metrics/system/telemetry'
SQL

  lambda {
    function_arn = aws_lambda_function.iot_to_timestream.arn
  }

#  role_arn = aws_iam_role.iot_to_timestream_role.arn

  error_action {
    cloudwatch_logs {
      log_group_name = "/aws/iot/errors"
      role_arn       = aws_iam_role.iot_to_timestream_role.arn
    }
  }

  depends_on = [
    aws_lambda_function.iot_to_timestream,
    aws_iam_role.iot_to_timestream_role,
    aws_iam_role_policy.iot_to_timestream_policy
  ]
}

resource "aws_lambda_permission" "iot_invoke" {
  statement_id  = "AllowIoTInvokeLambda"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.iot_to_timestream.function_name
  principal     = "iot.amazonaws.com"
  source_arn    = aws_iot_topic_rule.iot_lambda_rule.arn
}
