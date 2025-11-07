output "environment" {
  description = "Current environment"
  value       = var.environment
}

output "region" {
  description = "AWS region"
  value       = var.aws_region
}

output "bootstrap_bucket_name" {
  description = "Bootstrap S3 bucket name"
  value       = aws_s3_bucket.bootstrap.id
}

output "bootstrap_bucket_arn" {
  description = "Bootstrap S3 bucket ARN"
  value       = aws_s3_bucket.bootstrap.arn
}