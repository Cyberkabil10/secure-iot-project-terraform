terraform {
  required_version = ">= 1.5.0"

  backend "remote" {
    organization = "your-terraform-cloud-organization"

    workspaces {
      name = "secure-iot-project"
    }
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

