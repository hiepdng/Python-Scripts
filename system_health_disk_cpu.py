# Hiep, 11/20/2026
# This script is use to check disk and CPU threshold
# and email alerts.
#
# python ==3.13.5
####################################################
import shutil
import psutil
import smtplib
from email.message import EmailMessage

DISK_THRESHOLD = 85.0
CPU_THRESHOLD = 90.0

def check_system_health():
    # Check root partition usage
    total, used, free = shutil.disk_usage("/")
    disk_percent = (used / total) * 100
    
    # Check CPU load over a 1-second interval
    cpu_percent = psutil.cpu_percent(interval=1)

    alerts = []
    if disk_percent > DISK_THRESHOLD:
        alerts.append(f"CRITICAL: Root disk usage is at {disk_percent:.1f}%")
    if cpu_percent > CPU_THRESHOLD:
        alerts.append(f"WARNING: High CPU usage at {cpu_percent:.1f}%")

    if alerts:
        send_alert("\n".join(alerts))

def send_alert(body):
    # Example placeholder for local postfix/SMTP relay
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = "Server Health Alert"
    msg["From"] = "your_email@gmail.com"
    msg["To"] = "sysadmin@example.com"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("your_email@gmail.com", "your_app_password")
        server.send_message(msg)

if __name__ == "__main__":
    check_system_health()
