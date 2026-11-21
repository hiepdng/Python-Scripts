# Hiep, 11/20/2026
# This script will run commands on a list of computers using ssh.
#
# paramiko==5.1.0
# python ==3.13.5
#############################################################
import paramiko

SERVERS = ["10.0.1.10", 
           "10.0.1.11", 
           "10.0.1.12"]
USERNAME = "username"
KEY_PATH = "/home/usename/.ssh/id_ed25519"
COMMANDS = ["uname -r && uptime -p",
            "df -h",
            "ps -eo pid,user,%cpu,%mem,comm --sort=-%cpu | head -n 10",
            "ps -eo pid,comm,%mem,rss --sort=-%mem | head -n 10",
            "top -b -n 1 -o %CPU | head -n 17",
            "vmstat",
            "ip -br a"]

def run_command():
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

  for host in SERVERS:
    print("==============================")
    print(f"{host}")
    print("==============================")
    for cmd in COMMANDS:
      try:
        ssh.connect(host, username=USERNAME, key_filename=KEY_PATH, timeout=5)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        #output = stdout.read().decode().strip().replace("\n", "\n---------\n ")
        output = stdout.read().decode().strip()
        print(f"$ {cmd}\n{output}\n")
            
      except Exception as e:
        print(f"[{host}] Connection failed: {e}")
      finally:
        ssh.close()
    print("\n")


### main
if __name__ == "__main__":
  run_command()
