output "certificate_pem" {
  value     = aws_iot_certificate.cert.certificate_pem
  sensitive = true
}

output "private_key" {
  value     = aws_iot_certificate.cert.private_key
  sensitive = true
}

output "public_key" {
  value     = aws_iot_certificate.cert.public_key
  sensitive = true
}

output "iot_endpoint" {
  value = data.aws_iot_endpoint.iot.endpoint_address
}

output "grafana_url" {
  value = aws_grafana_workspace.secure_iot_grafana.endpoint
  description = "Access your Grafana dashboard using this URL"
}

