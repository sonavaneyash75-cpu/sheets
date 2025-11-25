# ==============================================================================
#  PRECAUTIONS AND PREREQUISITES 
# ==============================================================================

# 1.  ELEVATED PRIVILEGES REQUIRED:
#    - SNORT needs direct access to the network interface to capture packets.
#    - This script uses 'sudo' in the 'snort_command' list.
#    - You **MUST** run this Python script using 'sudo': 
#      $ sudo python3 snort_monitor.py
#    - Running as root is necessary but carries risk. Ensure your SNORT configuration 
#      and this Python script are trusted.

# 2.  SNORT INSTALLATION:
#    - SNORT must be correctly installed and configured on your system.
#    - Verify the 'SNORT_PATH' variable points to the correct executable location 
#      (e.g., /usr/sbin/snort).

# 3.  CONFIGURATION CHECK:
#    - The 'CONFIG_FILE' (/etc/snort/snort.conf) and 'INTERFACE' (e.g., eth0) 
#      variables MUST be updated to match your system environment.
#    - Check that the 'HOME_NET' variable in your snort.conf is correctly defined 
#      to cover the network you intend to protect.

# 4.  DOS RULES CHECK:
#    - Ensure your custom SNORT rules for DoS detection (e.g., SYN Flood, ICMP Flood) 
#      are correctly placed in your 'local.rules' file (or wherever your snort.conf 
#      references custom rules) AND are enabled.
#    - The Python script's detection logic relies on specific keywords 
#      (e.g., "SYN FLOOD") being in the rule's 'msg' field.

# 5.  ACTION LOGIC (Blocking IPs):
#    - The section within 'process_alert' for blocking IPs (e.g., using iptables) 
#      is currently commented out.
#    - **UNCOMMENT WITH CAUTION:** Automated blocking can lead to a **Self-DoS** #      (blocking legitimate traffic if the rule is too aggressive or triggers falsely).
#    - Always test detection rules extensively before enabling automatic response.

# ==============================================================================

import subprocess
import re
import time
from datetime import datetime

# --- Configuration ---
# Path to the snort executable and configuration file
SNORT_PATH = "/usr/sbin/snort" # Check your system's path!
CONFIG_FILE = "/etc/snort/snort.conf"
INTERFACE = "eth0" # Change to your network interface (e.g., 'eth0', 'ens33', 'wlan0')

# --- Snort Command ---
# -q: Quiet mode (don't show banner)
# -A console: Output alerts to console (stdout)
# -c: Configuration file
# -i: Interface to listen on
snort_command = [
    "sudo", SNORT_PATH, "-q", "-A", "console", 
    "-c", CONFIG_FILE, "-i", INTERFACE
]

# Regex to parse a SNORT alert line (adjust based on your SNORT version/output)
# This is a simplified regex to capture Timestamp, Message, and IP/Port info
ALERT_PATTERN = re.compile(
    r'(\d{2}/\d{2}-\d{2}:\d{2}:\d{2}\.\d+) ALERT: \[(.+?)\] \[.+?\] (.+?) \{(.+?)\} (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+) -> (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+)'
)

def process_alert(alert_line):
    """Parses an alert and takes a defined action."""
    match = ALERT_PATTERN.search(alert_line)
    
    if match:
        # Note: The group structure is based on the simplified regex
        timestamp = match.group(1)
        snort_msg = match.group(3)
        src_ip = match.group(5)
        src_port = match.group(6)
        dst_ip = match.group(7)
        dst_port = match.group(8)
        
        # --- DoS-Specific Action Logic ---
        if "SYN FLOOD" in snort_msg.upper() or "ICMP FLOOD" in snort_msg.upper():
            print("\n **DoS ALERT DETECTED!** ")
            print(f"Timestamp: {timestamp}")
            print(f"Attack Type: {snort_msg}")
            print(f"Source IP: {src_ip}")
            
            # **ACTION TO TAKE** (e.g., Block the IP using iptables/firewalld)
            #  NOTE: Uncomment the following lines only after careful testing 
            # try:
            #     # This command requires the Python script itself to be run with sudo
            #     subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", src_ip, "-j", "DROP"], check=True)
            #     print(f"*** ATTACKER IP {src_ip} BLOCKED VIA IPTABLES ***")
            # except subprocess.CalledProcessError as e:
            #     print(f"Error blocking IP {src_ip}: {e}")

            # Log to a separate file
            with open("dos_alerts.log", "a") as f:
                f.write(f"[{datetime.now().isoformat()}] DoS Detected from {src_ip} - Rule: {snort_msg}\n")
        
        else:
            # For non-DoS alerts, you might log or just print
            print(f"Standard Alert: {snort_msg}")
            
    else:
        # SNORT logs startup info and non-alert messages too; filter or ignore them.
        pass # print(f"Unmatched Line (not a clear alert): {line.strip()}")

def run_snort_and_monitor():
    """Starts SNORT and monitors its console output."""
    print(f"Starting SNORT on interface **{INTERFACE}**...")
    print(f"Command: {' '.join(snort_command)}")
    print("Monitoring output. Press Ctrl+C to stop.")
    
    try:
        # Start SNORT process
        process = subprocess.Popen(
            snort_command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            universal_newlines=True
        )

        # Continuously read and process output
        for line in iter(process.stdout.readline, ''):
            if "ALERT" in line:
                process_alert(line)
            
        process.stdout.close()
        process.wait()
        
    except FileNotFoundError:
        print(f"Error: SNORT executable not found at {SNORT_PATH}. Check your path.")
    except PermissionError:
        print("Error: Running SNORT requires root/sudo permissions. Rerun the Python script with 'sudo'.")
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
        if process.poll() is None:
            process.terminate()
            process.wait()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_snort_and_monitor()