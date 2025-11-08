# AlphaBrain Core – AWS Budget & Cost Control

Target: **$40/month average spend**, with alert thresholds at $40 (warning) and $50 (critical).

---

## 1. Budget Breakdown (Approx.)
| Resource | Description | Est. Monthly Cost |
|-----------|--------------|------------------|
| S3 Storage | Raw + processed datasets | $5-10 |
| RDS (Postgres) | Metadata and MLflow tracking | $5–10 |
| ECS / Fargate | API + model serving | $10–20 |
| EC2 (Airflow/Worker) | Batch pipeline jobs | $10–20 |
| Monitoring (CloudWatch, Grafana) | Metrics & logs | $1-5 |
| Total |  | **$50 avg. / $100 max** |

---

## 2. Cost Management Steps
1. Create AWS Budgets with monthly alerts (warning at $40, critical at $50).
2. Tag all resources with `project=alphabrain-core` for visibility.
3. Use Spot instances where possible (Airflow workers, ECS tasks).
4. Schedule auto-stop for idle EC2 instances.
5. Enable S3 lifecycle policies to archive old data.
6. Monitor usage via CloudWatch dashboards.

---

## 3. Cleanup Policy
- All experimental resources (non-production) must be cleaned up weekly.
- Delete unused S3 datasets and ECS tasks regularly.
- Review active budgets monthly.

---

## 4. Notes
AWS costs may vary by region and usage volume.  
Adjust thresholds accordingly and enforce limits before deploying compute-heavy jobs.
