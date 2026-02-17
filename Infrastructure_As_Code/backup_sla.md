# Backup SLA

## Coverage

We back up services that satisfy at least one of these criteria:
 - are primary source of truth for particular data
 - contain customer and/or client data
 - are not feasible (or very costly) to restore by other means

Services that are backed up:
 - MySQL
 - Prometheus
 - Loki

## Schedule

Times below are in UTC and triggered by cron on the respective hosts.

- MySQL:
	- 14:45 daily: `mysqldump agama` to `/home/backup/mysql/agama.sql` (on `mysql_backup_host`).
	- 15:00 Sundays: Duplicity full backup to `rsync://Bixu420@backup.<domain>/mysql`.
	- 15:10 Mon–Sat: Duplicity incremental backup to the same remote.
	- Expected completion: within 30 minutes (by 15:30).

- Prometheus:
	- 14:45 Sundays: trigger snapshot via Prometheus admin API (`/prometheus/api/v1/admin/tsdb/snapshot`).
	- 15:00 Sundays: Duplicity full backup of snapshot dir to `rsync://Bixu420@backup.<domain>/prometheus`.
	- 15:00 Mon–Sat: Snapshot + Duplicity incremental to the same remote.
	- 15:10 Sundays: cleanup old local snapshot directory.
	- Logs: `/home/backup/prometheus-backup.log`.

- Loki:
	- 14:45 Sundays: local rsync of `/tmp/loki/` to `/home/backup/loki/` and fix permissions.
	- 15:00 Sundays: Duplicity full backup to `rsync://Bixu420@backup.<domain>/loki`.
	- 15:10 Mon–Sat: Duplicity incremental backup to the same remote.
	- Logs: `/home/backup/loki-backup.log`.

All backups are started automatically by cron (see `roles/*/templates/backup-cron.j2`).

Backup RPO (recovery point objective):
- MySQL: daily (≤ 24 hours of data loss)
- Prometheus: daily (≤ 24 hours)
- Loki: daily (≤ 24 hours)



## Storage

- Remote: Duplicity uploads to `rsync://Bixu420@backup.<domain>/{mysql,prometheus,loki}`.
- Staging (local):
	- MySQL dump: `/home/backup/mysql/agama.sql`
	- Prometheus snapshots: `/var/lib/prometheus/metrics2/snapshots/`
	- Loki staged files: `/home/backup/loki/`
- Infrastructure and dashboards are versioned and mirrored via the internal Git server (this repository).

Backup data from both servers will be synchronized to an encrypted AWS S3 bucket in future (work in progress).


## Retention

- Current: No automated pruning is configured; all Duplicity chains (weekly full + daily incrementals) are retained until manual cleanup.
- Target policy (to be enforced): keep 4 weeks of backups per service (weekly full + daily incremental), using `duplicity remove-older-than 4W` and periodic `cleanup`.


## Usability checks

- MySQL: weekly test restore to a disposable database using `backup_restore.md` steps; daily `duplicity collection-status` check.
- Prometheus: weekly snapshot restore dry-run into a staging path and service restart validation; daily log review in `/home/backup/prometheus-backup.log`.
- Loki: weekly `duplicity verify` against the remote and spot-check restored files under a staging directory; daily log review in `/home/backup/loki-backup.log`.


## Restore process

Service is recovered from the backup in case of an incident, and when service cannot be restored in any other way.

RTO (recovery time objective) is:
 - 1 hour for MySQL
 - 2 hours for Prometheus
 - 2 hours for Loki

Detailed backup restore procedure is documented in the [backup_restore.md](./backup_restore.md).
