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

# MLflow outputs
output "mlflow_db_endpoint" {
  description = "MLflow RDS endpoint"
  value       = aws_db_instance.mlflow.endpoint
}

output "mlflow_db_name" {
  description = "MLflow database name"
  value       = aws_db_instance.mlflow.db_name
}

output "mlflow_artifacts_bucket" {
  description = "MLflow S3 artifacts bucket"
  value       = aws_s3_bucket.mlflow_artifacts.id
}

output "mlflow_db_secret_arn" {
  description = "ARN of secret containing DB password"
  value       = aws_secretsmanager_secret.mlflow_db_password.arn
  sensitive   = true
}