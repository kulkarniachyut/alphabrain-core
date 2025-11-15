# IAM user for Airflow to access S3
resource "aws_iam_user" "airflow" {
  name = "${var.project_name}-${var.environment}-airflow"

  tags = {
    Name    = "Airflow Service User"
    Purpose = "S3 data lake access"
  }
}

# Policy for S3 data lake access
resource "aws_iam_policy" "airflow_s3" {
  name        = "${var.project_name}-${var.environment}-airflow-s3"
  description = "Allow Airflow to read/write data lake"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket",
          "s3:GetBucketLocation"
        ]
        Resource = aws_s3_bucket.data_lake.arn
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Resource = "${aws_s3_bucket.data_lake.arn}/*"
      }
    ]
  })
}

# Attach policy to user
resource "aws_iam_user_policy_attachment" "airflow_s3" {
  user       = aws_iam_user.airflow.name
  policy_arn = aws_iam_policy.airflow_s3.arn
}

# Access key for Airflow (stored in Secrets Manager)
resource "aws_iam_access_key" "airflow" {
  user = aws_iam_user.airflow.name
}

# Store access key in Secrets Manager
resource "aws_secretsmanager_secret" "airflow_aws_credentials" {
  name = "${var.project_name}-${var.environment}-airflow-aws-credentials"
}

resource "aws_secretsmanager_secret_version" "airflow_aws_credentials" {
  secret_id = aws_secretsmanager_secret.airflow_aws_credentials.id
  secret_string = jsonencode({
    access_key_id     = aws_iam_access_key.airflow.id
    secret_access_key = aws_iam_access_key.airflow.secret
  })
}