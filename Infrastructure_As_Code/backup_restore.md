# Backup Restore Procedures

All restores are initiated from the Prometheus host while logged in as a privileged operator. The `backup` user owns the credentials and duplicity configuration, so every restore starts by switching to that user.

## MySQL

1. Switch to the backup user and clear the staging directory:
   ```bash
   sudo -iu backup
   rm -rf /home/backup/restore/*
   ```
2. Pull the most recent MySQL backup set from the backup server:
   ```bash
   duplicity --no-encryption restore rsync://Bixu420@backup.bixu.io/mysql /home/backup/restore/mysql
   ```
3. Stop MySQL before touching the data:
   ```bash
   sudo systemctl stop mysql
   ```
4. Restore the SQL dump into the target database (schema `agama` by default):
   ```bash
   mysql agama < /home/backup/restore/mysql/agama.sql
   ```
5. Start MySQL and watch the logs for errors:
   ```bash
   sudo systemctl start mysql
   sudo journalctl -u mysql -n 200 -f
   ```

## Prometheus

1. Switch to the backup user and ensure the staging directory is empty:
   ```bash
   sudo -iu backup
   rm -rf /home/backup/restore/*
   ```
2. Download the latest Prometheus snapshot set. Use `--no-restore-ownership` to avoid ownership errors because the `backup` user cannot chown files to `prometheus:prometheus`:
   ```bash
   duplicity --no-encryption --no-restore-ownership restore rsync://Bixu420@backup.bixu.io/prometheus /home/backup/restore/prometheus
   ```
3. Identify the snapshot directory that duplicity restored. The archive keeps the original `snapshots/<snapshot_id>` hierarchy, so you should end up with `/home/backup/restore/prometheus/snapshots/20251102T121036Z-0cbfa62747afb9e5` (replace the timestamp/hash with whatever you actually restored).
4. Stop Prometheus and move only the TSDB files (not the `snapshots` directory) into `/var/lib/prometheus/metrics2/`:
   ```bash
   sudo systemctl stop prometheus
   sudo rm -rf /var/lib/prometheus/metrics2/*
   sudo cp -a /home/backup/restore/prometheus/snapshots/<snapshot_id>/* /var/lib/prometheus/metrics2/
   sudo chown -R prometheus:prometheus /var/lib/prometheus/metrics2
   ```
5. Start Prometheus and confirm that the metrics UI shows the expected time range:
   ```bash
   sudo systemctl start prometheus
   sudo journalctl -u prometheus -n 200 -f
   ```
6. When Prometheus is healthy again, clean up the staging directory:
   ```bash
   rm -rf /home/backup/restore/*
   ```
