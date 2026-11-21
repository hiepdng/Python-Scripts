# Hiep, 11/21/2026
# This script is an example of backup audit log files to a 
# different location and clean up /var/log/autdit files
#
# python ==3.13.5
#########################################################
import time
import tarfile
from pathlib import Path

LOG_DIR = Path("/var/log/audit")
ARCHIVE_DIR = Path("/var/backups/audit_logs")
RETENTION_DAYS = 7

def archive_old_logs():
  ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
  cutoff_time = time.time() - (RETENTION_DAYS * 86400)
    
  archive_name = ARCHIVE_DIR / f"logs_{time.strftime('%Y%m%d')}.tar.gz"
  old_files = [f for f in LOG_DIR.glob("*.log.*") if f.stat().st_mtime < cutoff_time]

  if not old_files:
    return

  with tarfile.open(archive_name, "w:gz") as tar:
    for file_path in old_files:
      tar.add(file_path, arcname=file_path.name)

  print(f"Archived and removed {len(old_files)} old log files.")


### main
if __name__ == "__main__":
  archive_old_logs()
