# S3 bucket for MLflow artifacts
resource "aws_s3_bucket" "mlflow_artifacts" {
  bucket = "${var.project_name}-${var.environment}-mlflow-artifacts"
  
  tags = {
    Name = "MLflow Artifacts"
  }
}

# Block public access
resource "aws_s3_bucket_public_access_block" "mlflow_artifacts" {
  bucket = aws_s3_bucket.mlflow_artifacts.id
  
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Versioning for artifact recovery
resource "aws_s3_bucket_versioning" "mlflow_artifacts" {
  bucket = aws_s3_bucket.mlflow_artifacts.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

# Random password for RDS
resource "random_password" "mlflow_db" {
  length  = 32
  special = true
}

# Store password in Secrets Manager
resource "aws_secretsmanager_secret" "mlflow_db_password" {
  name = "${var.project_name}-${var.environment}-mlflow-db-password"
}

resource "aws_secretsmanager_secret_version" "mlflow_db_password" {
  secret_id     = aws_secretsmanager_secret.mlflow_db_password.id
  secret_string = random_password.mlflow_db.result
}

# RDS Postgres for MLflow metadata
resource "aws_db_instance" "mlflow" {
  identifier        = "${var.project_name}-${var.environment}-mlflow"
  engine            = "postgres"
  engine_version    = "15"
  instance_class    = "db.t4g.micro"
  allocated_storage = 20
  storage_type      = "gp3"
  
  db_name  = "mlflow"
  username = "mlflow"
  password = random_password.mlflow_db.result
  
  publicly_accessible    = true  # For testing - secure later
  skip_final_snapshot    = true  # Dev only
  backup_retention_period = 7
  
  vpc_security_group_ids = [aws_security_group.mlflow_db.id]
  
  tags = {
    Name = "MLflow Database"
  }
}

# Security group for RDS
resource "aws_security_group" "mlflow_db" {
  name        = "${var.project_name}-${var.environment}-mlflow-db"
  description = "Allow Postgres access"
  
  ingress {
    description = "PostgreSQL from anywhere (dev only)"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # TODO: Restrict to your IP
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "MLflow DB Security Group"
  }
}
