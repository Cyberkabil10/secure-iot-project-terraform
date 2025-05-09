terraform {
  required_version = ">= 1.5.0"

  cloud { 
    
    organization = "pfa-iot-project" 

    workspaces { 
      name = "aws-infra" 
    } 
  } 

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

