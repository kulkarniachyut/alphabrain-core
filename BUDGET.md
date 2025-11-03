# AlphaBrain Core – AWS Budget & Cost Control

Target: **$150/month average spend**, with alert thresholds at $100 (warning) and $200 (critical).

---

## 1. Budget Breakdown (Approx.)
| Resource | Description | Est. Monthly Cost |
|-----------|--------------|------------------|
| S3 Storage | Raw + processed datasets | $10–20 |
| RDS (Postgres) | Metadata and MLflow tracking | $20–40 |
| ECS / Fargate | API + model serving | $30–70 |
| EC2 (Airflow/Worker) | Batch pipeline jobs | $20–50 |
| Monitoring (CloudWatch, Grafana) | Metrics & logs | $10–20 |
| Total |  | **$150 avg. / $200 max** |

---

## 2. Cost Management Steps
1. Create AWS Budgets with monthly alerts (warning at $100, critical at $200).
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
