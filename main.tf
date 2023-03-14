terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }
}

data "aws_caller_identity" "current" {}

provider "aws" {
  profile = "default"
  region  = "ap-southeast-1"
}

