# ICA0002 — Infrastructure Services (Ansible / IaC)

This repository contains my hands-on infrastructure engineering work for **ICA0002 (IT Infrastructure Services)**.  
The environment is provisioned and configured using **Ansible (Infrastructure as Code)** and includes a small, highly available service stack with **DNS, databases, load balancing, observability, and backups**.

> Goal: build a reproducible, automated infrastructure setup (Linux-first) with high availability, monitoring, logging, redundancy, and documented recovery procedures.

---

## What’s in the lab stack

### Core services
- **DNS**: BIND9 + dynamic DNS updates (nsupdate)
- **Web application**: *Agama* deployed as multiple **Docker containers**
- **Database**: **MySQL** (primary/secondary behavior via read_only)
- **Load balancing**: **HAProxy**
- **High availability**: **Keepalived (VRRP)** with HAProxy health checks

### Observability
- **Prometheus** (metrics)
- **Loki** (logs)
- **Grafana** (dashboards + provisioning)
- Exporters:
  - node-exporter
  - mysqld-exporter
  - haproxy-exporter
  - nginx-exporter
  - bind exporter
  - keepalived exporter
- **Promtail** ships logs to Loki

### Backups / Recovery
- Automated backups using **Duplicity**
- Backup policy + objectives documented:
  - `backup_sla.md` (RPO/RTO, schedule, retention target)
  - `backup_restore.md` (step-by-step restore procedures)
- Service SLO example:
  - `slo.md` (SLI/SLO for the Agama service using Prometheus/Loki/Grafana)


