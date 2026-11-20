# Hiep, 11/20/2026
# This scripts used to check systemd services. 
# It will restart the service if it is stop and email
# alerts.
# python ==3.13.5
# 
######################################################
import subprocess
import smtplib
from email.message import EmailMessage

def get_service_state(service_name: str) -> str:
    result = subprocess.run(
        ["systemctl", "is-active", service_name],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()  #active/inactive

def send_alert(body):
  # Email message
  msg = EmailMessage()
  msg["From"] = "your_email@gmail.com"
  msg["To"] = "sysadmin@example.com"
  msg["Subject"] = "Web Endpoint Alert"
  msg.set_content(body) 

  ### Send email message with local sendmail binary
  #subprocess.run(
  #  ["/usr/sbin/sendmail", "-t", "-oi"],
  #  input=msg.as_bytes(),
  #  check=True
  #)
  ###or Send email message with gamil smtp server
  with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login("your_email@gmail.com", "your_app_password")
    server.send_message(msg)



### main
services = ["ssh.service",
            "atd.service",
            "cron.service",
            "docker.service",
            "NetworkManager.service",
            "systemd-journald.service"]

alerts = []
for service in services:
  state = get_service_state(service)
  if state == "inactive":
    result = subprocess.run(["systemctl", "restart", service], check=True)
    status_code = result.returncode
    alerts.append(f"{service} is not running. State: {state}. Restart {service}... with status code: {status_code}")

###send email to alert
if alerts:
  send_alert("\n".join(alerts))
