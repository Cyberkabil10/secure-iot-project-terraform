data "aws_iot_endpoint" "iot" {
  endpoint_type = "iot:Data-ATS"
}

resource "aws_iot_thing" "iot_client" {
  name = "MySecureIoTClient"
}

resource "aws_iot_certificate" "cert" {
  active = true
}

resource "aws_iot_thing_principal_attachment" "attach_cert" {
  thing     = aws_iot_thing.iot_client.name
  principal = aws_iot_certificate.cert.arn
}

resource "aws_iot_policy" "iot_policy" {
  name = "SecureIoTPolicy"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Action = [
        "iot:Connect",
        "iot:Publish",
        "iot:Subscribe",
        "iot:Receive"
      ],
      Resource = "*"
    }]
  })
}

resource "aws_iot_policy_attachment" "attach_policy" {
  policy = aws_iot_policy.iot_policy.name
  target = aws_iot_certificate.cert.arn
}
