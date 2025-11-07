provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "demo" {
  bucket = "alphabrain-core-demo-bucket"
  
  tags = {
    project = "alphabrain-core"
    env     = "dev"
  }
}

resource "aws_s3_bucket_ownership_controls" "demo" {
  bucket = aws_s3_bucket.demo.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "demo" {
  depends_on = [aws_s3_bucket_ownership_controls.demo]
  
  bucket = aws_s3_bucket.demo.id
  acl    = "private"
}
