# AlphaBrain Core — Week 0 Setup Log & Environment Blueprint

**Objective:**  
Establish a reproducible, secure, AWS-backed engineering environment for AlphaBrain Core — covering repository governance, IAM, billing, tagging, storage, and observability.  
This document serves as the **single source of truth** for how the base infrastructure was originally created and configured.

---

## 🧠 Project Identity
| Component | Value |
|------------|--------|
| **Project Name** | AlphaBrain Core |
| **Namespace / Tag Prefix** | `alphabrain-core` |
| **AWS Region** | `us-east-1` |
| **GitHub Repo** | `alphabrain-core` |
| **Environment Tags** | `env=dev`, `project=alphabrain-core`, `owner=<your name>`, `cost-center=ai-lab` |
| **Primary Goal** | Build a production-grade AI Engineering platform using AWS and open source |

---

## 🗂️ 1. Repository Configuration

### Repos & Branching
- **Repo Name:** `alphabrain-core`
- **Main Branches:**
  - `main` → stable production
  - `dev` → active integration
  - `feature/*` → short-lived features or experiments
- **Branch Protection Rules:**
  - Require PR before merge (for `main` and `dev`)
  - Require linear history
  - Dismiss stale reviews
  - Block force pushes

### GitHub Standards
- `.github/PULL_REQUEST_TEMPLATE.md` — PRs must describe purpose, changes, verification.
- **Commit Convention:** [Conventional Commits](https://www.conventionalcommits.org/)
  - Example: `feat(airflow): add DAG for stock ingestion`
- **License:** MIT
- **Main Docs:**  
  - `README.md` — overview  
  - `GOVERNANCE.md` — ethics, conduct  
  - `BUDGET.md` — cost management  
  - `.gitignore` — Python + AWS + data-specific  

---

## 🔐 2. IAM Configuration

### IAM Users
| User | Description | Policies | MFA | CLI Profile |
|-------|-------------|-----------|------|-------------|
| `alphabrain-admin` | Setup & Infrastructure control user | `AdministratorAccess` | ✅ | `alphabrain` |
| `alphabrain-dev` | Day-to-day operations & CI/CD | Custom `AlphaBrainDevPolicy` (least privilege) | ✅ | `alphabrain-dev` |

### IAM Policy: AlphaBrainDevPolicy
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3Access",
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::alphabrain-core-*",
        "arn:aws:s3:::alphabrain-core-*/*"
      ]
    },
    {
      "Sid": "ECSAccess",
      "Effect": "Allow",
      "Action": ["ecs:Describe*", "ecs:List*", "ecs:RunTask", "ecs:StartTask", "ecs:StopTask"],
      "Resource": "*"
    },
    {
      "Sid": "CloudWatchAccess",
      "Effect": "Allow",
      "Action": [
        "cloudwatch:GetMetricData",
        "cloudwatch:ListMetrics",
        "logs:GetLogEvents",
        "logs:FilterLogEvents"
      ],
      "Resource": "*"
    },
    {
      "Sid": "ECRReadAccess",
      "Effect": "Allow",
      "Action": [
        "ecr:Describe*",
        "ecr:GetAuthorizationToken",
        "ecr:BatchGetImage",
        "ecr:GetDownloadUrlForLayer"
      ],
      "Resource": "*"
    }
  ]
}
```

### Profiles Configured
```bash
aws configure --profile alphabrain
aws configure --profile alphabrain-dev
```

Verification:
```bash
aws sts get-caller-identity --profile alphabrain
aws sts get-caller-identity --profile alphabrain-dev
```

---

## 💰 3. Billing, Budgets, and Alerts

### Monthly Budget
| Setting | Value |
|----------|--------|
| Budget Name | `AlphaBrain-Monthly-Budget` |
| Type | Cost budget |
| Amount | $150/month |
| Region | Global |
| Alerts | $100 (Warning), $200 (Critical) |
| Notification | Email → <your email> |

### Cost Anomaly Detection
- Created under **Billing → Anomaly Detection**
- Monitors total spend tagged with `project=alphabrain-core`
- Sensitivity: Medium
- Notification channel: Email

---

## 🏷️ 4. Tagging & Cost Allocation

### Tags Created (via Resource Explorer)
| Key | Value | Applied To |
|-----|--------|------------|
| `project` | `alphabrain-core` | All |
| `owner` | `<your name>` | All |
| `env` | `dev` | All |
| `cost-center` | `ai-lab` | Optional |

### Tag Activation
Activated under **Billing → Cost Allocation Tags**  
(visible in Cost Explorer after ~24 hrs).

### Tag Usage Example (Terraform/AWS CLI)
```bash
--tags project=alphabrain-core owner=<your name> env=dev
```

---

## 🪣 5. S3 Bucket — Logs & Artifacts

| Setting | Value |
|----------|--------|
| Bucket Name | `alphabrain-core-logs` |
| Region | `us-east-1` |
| Access | Private (all public access blocked) |
| Versioning | Enabled |
| Encryption | AES-256 |
| Lifecycle Rules | IA @30 days → Glacier @90 days |
| Tags | `project`, `owner`, `env` |

### CLI Verification
```bash
aws s3 ls s3://alphabrain-core-logs --profile alphabrain-dev
echo "alpha test" > test.txt
aws s3 cp test.txt s3://alphabrain-core-logs/test.txt --profile alphabrain-dev
```

---

## 📊 6. CloudWatch Dashboard & Monitoring

| Component | Metric | Namespace | Region | Notes |
|------------|---------|------------|---------|--------|
| **Billing Widget** | EstimatedCharges (USD) | `AWS/Billing` | `us-east-1` | Required for global cost view |
| **S3 Storage Widget** | BucketSizeBytes | `AWS/S3` | `us-east-1` | Tracks `alphabrain-core-logs` |
| **ECS (Placeholder)** | CPUUtilization, MemoryUtilization | `AWS/ECS` | `us-east-1` | Active post Week 2 infra setup |

Dashboard: **`alphabrain-monitor`**

### CloudWatch Alarm
| Name | Metric | Threshold | Action |
|------|---------|------------|--------|
| `AlphaBrainCostAlert` | EstimatedCharges (USD) | > $150 | Email alert |

---

## ⚙️ 7. AWS Resource Namespace & Structure

| Resource Type | Naming Convention | Example |
|----------------|-------------------|----------|
| S3 Buckets | `alphabrain-core-*` | `alphabrain-core-logs` |
| IAM Users | `alphabrain-*` | `alphabrain-admin`, `alphabrain-dev` |
| IAM Policies | `AlphaBrain*Policy` | `AlphaBrainDevPolicy` |
| ECS Cluster | `alphabrain-core-cluster` | (Week 2) |
| CloudWatch Dashboard | `alphabrain-monitor` |  |
| Terraform State | `alphabrain-core-tfstate` | (Week 1) |

---

## 🧩 8. CLI Environment Reference

### AWS CLI Version
```bash
aws --version
# Example: aws-cli/2.17.x Python/3.11.x Darwin/arm64
```

### Credentials File Structure
```
~/.aws/credentials
[alphabrain]
aws_access_key_id = AKIAxxxxxxxxxxxx
aws_secret_access_key = abc123xyz...

[alphabrain-dev]
aws_access_key_id = AKIAyyyyyyyyyyyy
aws_secret_access_key = def456uvw...
```

### Config File
```
~/.aws/config
[profile alphabrain]
region = us-east-1
output = json

[profile alphabrain-dev]
region = us-east-1
output = json
```

---

## 🧭 9. Current Status Summary

| Category | State | Verification |
|-----------|--------|--------------|
| GitHub Repo Setup | ✅ | Protected branches, PR template |
| IAM & MFA | ✅ | Profiles verified |
| Budget & Alerts | ✅ | Billing + Anomaly detection configured |
| Tagging | ✅ | Active, visible in Cost Explorer |
| Storage | ✅ | Encrypted + versioned bucket |
| CloudWatch | ✅ | Dashboard and alarm created |

---

## 🏁 Week 0 Completion Statement
✅ **AlphaBrain Core foundational environment fully established.**  
This configuration supports all future IaC, data, and agentic system builds.  
Recreating this environment is possible by following this document alone.

---

> **Next Step (Week 1):**  
> Initialize Infrastructure as Code (Terraform base), setup remote state backend on the above S3 bucket, and integrate GitHub Actions CI pipeline for IaC validation.
