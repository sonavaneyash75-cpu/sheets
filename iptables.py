import subprocess

def run_iptables(command):
    """Executes an iptables command using sudo."""
    try:
        # Prepend 'sudo' to the command list
        subprocess.run(
            ['sudo'] + command, 
            check=True,  # Raise error on failure
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        print(f" Rule successful: {' '.join(command)}")
    except subprocess.CalledProcessError as e:
        print(f" Rule failed: {' '.join(command)}")
        print(f"Error: {e.stderr.decode().strip()}")
    except FileNotFoundError:
        print(" Error: 'sudo' or 'iptables' command not found.")
    except Exception as e:
        print(f" Unexpected Error: {e}")

# --- 1. Block the Class C Network (192.168.1.0/24) ---
# Blocks all traffic from this source network using DROP (silent discard).
run_iptables([
    'iptables', 
    '-A', 'INPUT',  # Append to INPUT chain
    '-s', '192.168.1.0/24', # Source Network (Class C)
    '-j', 'DROP' 
])

# --- 2. Block Port 22 (SSH) ---
# Blocks all incoming TCP traffic on destination port 22 using REJECT.
run_iptables([
    'iptables', 
    '-A', 'INPUT',  # Append to INPUT chain
    '-p', 'tcp',    # Protocol TCP
    '--dport', '22', # Destination Port 22
    '-j', 'REJECT'
])

print("\n---  Configuration Complete ---")
print("To verify rules, run: sudo iptables -L INPUT --line-numbers")
print("To flush (clear) all rules, run: sudo iptables -F")
