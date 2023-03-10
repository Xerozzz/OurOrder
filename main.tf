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

# Creating IAM Role for CodeDeploy
resource "aws_iam_role" "codedeploy" {
  name = "codedeploy_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "codedeploy.amazonaws.com"
        }
      }
    ]
  })
}

# Creating IAM Policy attachment for CodeDeploy
resource "aws_iam_role_policy_attachment" "codedeploy_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AWSCodeDeployRole"
  role       = aws_iam_role.codedeploy.name
}

# Create S3 Bucket
resource "aws_s3_bucket" "s3_bucket" {
  bucket = "s3_bucket"
}

# Create S3 Block all Public access
resource "aws_s3_bucket_public_access_block" "block_public_acls" {
  bucket = aws_s3_bucket.s3_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Create IAM Policy to access S3 bucket
# resource "aws_iam_policy" "s3_policy" {
#   name        = "s3_bucket_policy"
#   policy      = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Effect   = "Allow"
#         Action   = [
#           "s3:Get*",
#           "s3:List*"
#         ]
#         Resource = "${aws_s3_bucket.s3_bucket.arn}/*"
#       }
#     ]
#   })
# }

# Create IAM User for Lightsail
resource "aws_iam_user" "lightsail_user" {
  name = "lightsail_user"
}

# Create access keys for the user
resource "aws_iam_access_key" "lightsail_user_key" {
  user = aws_iam_user.lightsail_user.name
}

# Create the lightsail instance
resource "aws_lightsail_instance" "lightsail_instance" {
  name              = "lightsail_instance"
  availability_zone = "ap-southeast-1a"
  blueprint_id      = "amazon_linux_2"
  bundle_id         = "nano_2_0"

  user_data = <<-EOF
              #!/bin/bash
              mkdir /etc/codedeploy-agent/
              mkdir /etc/codedeploy-agent/conf
              cat <<EOT >> /etc/codedeploy-agent/conf/codedeploy.onpremises.yml
              ---
              aws_access_key_id: ${aws_iam_access_key.lightsail_user_key.id}
              aws_secret_access_key: ${aws_iam_access_key.lightsail_user_key.secret}
              iam_user_arn: ${aws_iam_user.lightsail_user.name}
              region: ap-southeast-1
              EOT
              sudo yum update
              sudo yum install ruby -y 
              sudo yum install wget -y 
              wget https://aws-codedeploy-us-west-2.s3.us-west-2.amazonaws.com/latest/install
              chmod +x ./install
              sudo ./install auto
              EOF
}

# Register Lightsail with CodeDeploy
resource "null_resource" "register_lightsail_instance" {
  provisioner "local-exec" {
    command = "aws deploy register-on-premises-instance --instance-name ${aws_lightsail_instance.lightsail_instance.name} --iam-user-arn arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/${aws_iam_user.lightsail_user.name} --region ap-southeast-1 --tags Key=Name,Value=CodeDeployLightsail"
  }
}

# Create CodeDeploy application
resource "aws_codedeploy_app" "my_app" {
  name = "my-app"
}

# Create deployment group
resource "aws_codedeploy_deployment_group" "my_deployment_group" {
  app_name              = aws_codedeploy_app.my_app.name
  deployment_group_name = "my-deployment-group"
  service_role_arn      = aws_iam_role.codedeploy.arn

  ec2_tag_set {
    ec2_tag_filter {
      key   = "Name"
      type  = "KEY_AND_VALUE"
      value = "CodeDeployLightsail"
    }
  }
}

# Define variables
variable "github_repo" {
  type        = string
  default     = "Xerozzz/OurOrder"
  description = "The name of the public GitHub repository containing the Flask application"
}

# Create a CodePipeline that deploys the Flask application to the Lightsail instance using CodeDeploy
resource "aws_codepipeline" "pipeline" {
  name     = "pipeline"
  role_arn = aws_iam_role.codedeploy.arn

  artifact_store {
    location = aws_s3_bucket.s3_bucket.bucket
    type     = "S3"
  }

  stage {
    name = "Source"

    action {
      name             = "Source"
      category         = "Source"
      owner            = "ThidParty"
      provider         = "GitHub"
      version          = "1"
      output_artifacts = ["source_output"]

      configuration = {
        Owner                = "Public"
        Repo                 = var.github_repo
        Branch               = "main"
        PollForSourceChanges = "true"
      }
    }
  }

  stage {
    name = "Deploy"

    action {
      name             = "Deploy"
      category         = "Deploy"
      owner            = "AWS"
      provider         = "CodeDeployToLightsail"
      version          = "1"
      input_artifacts  = ["build_output"]
      output_artifacts = []
      configuration = {
        ApplicationName     = aws_codedeploy_app.my_app.name
        DeploymentGroupName = aws_codedeploy_deployment_group.my_deployment_group.deployment_group_name
      }
    }
  }
}