resource "aws_iam_role" "iot_to_timestream_role" {
  name = "iot-to-timestream-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "iot.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "iot_to_timestream_policy" {
  name = "iot-to-timestream-policy"
  role = aws_iam_role.iot_to_timestream_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "timestream:WriteRecords"
        ],
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "lambda:InvokeFunction"
        ],
        Resource = aws_lambda_function.iot_to_timestream.arn
      }
    ]
  })
}
