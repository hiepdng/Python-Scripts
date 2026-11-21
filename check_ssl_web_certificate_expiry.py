# Hiep, 11/21/2026
# This script is used to check SSL web certificate for
# expiration day threshold and email alerts.
#
# python ==3.13.5
####################################################
import datetime
import socket
import ssl
from cryptography import x509
from email.message import EmailMessage

HOSTNAMES = ["google.com",
             "yahoo.com",
             "dms.adrc.washington.edu"]
PORT = 443
WARN_DAYS = 30

def get_cert_details(host, port=443):
  context = ssl.create_default_context()
  context.check_hostname = False
  context.verify_mode = ssl.CERT_NONE

  with socket.create_connection((host, port), timeout=10) as sock:
    with context.wrap_socket(sock, server_hostname=host) as ssock:
      der_cert = ssock.getpeercert(binary_form=True)

  cert = x509.load_der_x509_certificate(der_cert)
  expiry = cert.not_valid_after_utc
  days_left = (expiry - datetime.datetime.now(datetime.timezone.utc)).days

  print(f"Host:       {host}")
  print(f"Issuer:     {cert.issuer.rfc4514_string()}")
  print(f"Expires:    {expiry.strftime('%Y-%m-%d %H:%M:%S UTC')}")
  print(f"Days Left:  {days_left}\n")
 
  if days_left <= WARN_DAYS:
    alerts.append(f"WARNING: Host:       {host}")
    alerts.append(f"       : Issuer:     {cert.issuer.rfc4514_string()}")
    alerts.append(f"       : Expires:    {expiry.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    alerts.append(f"       : Days Left:  {days_left}\n")


def send_alert(body):
  # Email message
  msg = EmailMessage()
  msg["From"] = "your_email@gmail.com"
  msg["To"] = "sysadmin@example.com"
  msg["Subject"] = "Web Certificate Expiry Alert"
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
alerts = []
if __name__ == "__main__":
  for host in HOSTNAMES:
    print("--------------")
    get_cert_details(host)

  if alerts:
    send_alert("\n".join(alerts))

