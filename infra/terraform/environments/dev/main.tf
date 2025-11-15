provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      project     = var.project_name
      environment = var.environment
      managed-by  = "terraform"
    }
  }
}

# Bootstrap test resource
resource "aws_s3_bucket" "bootstrap" {
  bucket = "${var.project_name}-${var.environment}-bootstrap"
}

resource "aws_s3_bucket_versioning" "bootstrap" {
  bucket = aws_s3_bucket.bootstrap.id

  versioning_configuration {
    status = "Enabled"
  }
} # Trigger test
# Terraform test
