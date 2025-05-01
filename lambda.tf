# lambda.tf
resource "aws_lambda_function" "iot_to_timestream" {
  filename         = "lambda_payload.zip"
  function_name    = "IoTTelemetryToTimestream"
  role             = aws_iam_role.lambda_exec_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.9"
  source_code_hash = filebase64sha256("lambda_payload.zip")
}
