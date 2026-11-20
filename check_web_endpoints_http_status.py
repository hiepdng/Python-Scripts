# Hiep, 11/20/2026
# This scripts used to check all webpages and email
# to you with HTTP status of each webpage.
#
# python ==3.13.5
######################################################
from http import HTTPStatus
import requests
import subprocess
import smtplib
from email.message import EmailMessage

urls = ["http://localhost:9090/metrics",
        "https://www.google.com",
        "https://www.marketwatch.com",
        "https://www.yahoo.com",
        "https://httpbin.org",
        "https://httpbin.org",
        "https://httpbin.org",
        "https://httpbin.org",
        "https://httpbin.org",
        "https://example.invalid",
        "https://www.lklkcom/",
        "https://www.marketwatch.com"]

alerts = []

def check_url_status(url: str, follow_redirects: bool = False):
  try:
    # allow_redirects=False ensures 3xx codes (301, 302, etc.) are caught directly
    response = requests.get(url, allow_redirects=follow_redirects, timeout=10)
    code = response.status_code

    # Look up the standard human-readable phrase and description
    try:
      status_info = HTTPStatus(code)
      phrase = status_info.phrase
      description = status_info.description
    except ValueError:
      # Handles non-standard or custom server status codes (e.g., 418, 599)
      phrase = "Non-Standard Status Code"
      description = "Custom or unrecognized HTTP status."

    # Categorize by status class
    if 100 <= code < 200:
      category = "Informational"
    elif 200 <= code < 300:
      category = "Success"
    elif 300 <= code < 400:
      category = f"Redirection -> {response.headers.get('Location', 'Unknown target')}"
    elif 400 <= code < 500:
      category = "Client Error"
    elif 500 <= code < 600:
      category = "Server Error"
    else:
      category = "Unknown Category"

    #print(f"[{code} {phrase}] ({category}) - {url}")
    alerts.append(f"[{code} {phrase}] ({category}) - {url}")
    # Uncomment below if you want the full explanation printed too:
    #print(f"   Details: {description}")

  except requests.exceptions.Timeout:
    #print(f"[TIMEOUT] Request timed out - {url}")
    alerts.append(f"[TIMEOUT] Request timed out - {url}")
  except requests.exceptions.SSLError:
    #print(f"[SSL ERROR] Certificate verification failed - {url}")
    alerts.append(f"[SSL ERROR] Certificate verification failed - {url}")
  except requests.exceptions.ConnectionError:
    #print(f"[CONNECTION ERROR] Could not reach server - {url}")
    alerts.append(f"[CONNECTION ERROR] Could not reach server - {url}")
  except requests.exceptions.RequestException as e:
    #print(f"[REQUEST FAILED] {e} - {url}")
    alerts.append(f"[REQUEST FAILED] {e} - {url}")


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
if __name__ == "__main__":
  for url in urls:
    check_url_status(url, follow_redirects=False)

  #send email to alert
  if alerts:
    send_alert("\n".join(alerts))
