# AlphaBrain Core – Governance & Ethics

This document defines the governance, ethics, and compliance rules for the AlphaBrain Core project.

---

## 1. Code of Conduct
- Follow professional and respectful communication standards.
- Commit messages and documentation must be clear, concise, and reproducible.
- All experimental branches must include short rationales for significant architectural changes.

---

## 2. Ethical Principles
- No trading automation or financial decision-making will be executed directly.
- AI outputs are **non-binding suggestions** for demonstration only.
- All external data sources must have transparent licensing and usage rights.

---

## 3. Data Licensing & Compliance Checklist
| Item | Description | Status |
|------|--------------|--------|
| Dataset source verified | Confirm data is public or licensed for research. | ☐ |
| Terms of service reviewed | Review provider’s terms. | ☐ |
| PII handling reviewed | Ensure no personal or sensitive data is used. | ☐ |
| Attribution documented | Cite data providers in documentation. | ☐ |

---

## 4. Experiment Governance
- Each experiment run must have a run ID and configuration file stored in `experiments/`.
- Use MLflow for experiment tracking and model lineage.
- No experiments should exceed AWS budget constraints (see `BUDGET.md`).

---

## 5. Safety & Reproducibility
- All deployed services must have rollback configurations.
- Maintain IaC (Terraform) for reproducibility.
- Use AWS Secrets Manager for credentials and environment variables.
