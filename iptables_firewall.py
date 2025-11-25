import subprocess
import sys

def execute_iptables_command(command):
    """Executes a single iptables command."""
    try:
        # Use subprocess.run to execute the command.
        # check=True raises an exception if the command fails.
        # capture_output=True captures stdout/stderr.
        result = subprocess.run(
            ['sudo'] + command,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ Success: {' '.join(command)}")
        # print(f"Output:\n{result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing command: {' '.join(command)}")
        print(f"Return Code: {e.returncode}")
        print(f"Stderr:\n{e.stderr.strip()}")
        return False
    except FileNotFoundError:
        print("❌ Error: 'sudo' or 'iptables' command not found. Ensure iptables is installed.")
        return False
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return False

def configure_firewall_rules():
    """Applies the specific iptables rules requested by the user."""
    
    # ⚠️ WARNING: These rules will be applied immediately. 
    # Blocking port 22 might lock you out if you're using SSH.
    # Always test in a safe, controlled environment.
    
    print("--- ⚙️ Configuring Firewall Rules ---")

    # --- Rule 1: Blocking a Class C Network (e.g., 192.168.1.0/24) ---
    # This rule blocks ALL traffic from the specified source network.
    class_c_network_to_block = '192.168.1.0/24' 
    rule_1 = [
        'iptables', 
        '-A', 'INPUT', # Append to the INPUT chain
        '-s', class_c_network_to_block, # Source (a Class C network)
        '-j', 'DROP' # Action: Drop the packets silently
    ]
    execute_iptables_command(rule_1)

    # --- Rule 2: Blocking Port 22 (SSH) ---
    # This rule blocks ALL incoming traffic destined for the machine's port 22.
    port_to_block = '22'
    rule_2 = [
        'iptables', 
        '-A', 'INPUT', # Append to the INPUT chain
        '-p', 'tcp', # Protocol: TCP
        '--dport', port_to_block, # Destination port: 22
        '-j', 'REJECT' # Action: Reject (sends an ICMP error back)
    ]
    execute_iptables_command(rule_2)
    
    print("\n--- ✅ Rules Applied ---")
    print("Run 'sudo iptables -L' to view the active rules.")
    
    # --- Optional: Flush/Clear all rules (for cleanup/testing) ---
    # print("\n--- 🗑️ Clearing All Rules (Uncomment to use) ---")
    # execute_iptables_command(['iptables', '-F'])
    # execute_iptables_command(['iptables', '-X'])
    # execute_iptables_command(['iptables', '-Z'])

if __name__ == "__main__":
    # Ensure the script is run with the necessary privileges (though the commands use 'sudo')
    # and that you understand the risks.
    
    print("WARNING: This script will execute commands with 'sudo' to modify system firewall rules.")
    print("Execute this script only if you are aware of the consequences.")
    
    if len(sys.argv) > 1 and sys.argv[1].lower() == 'run':
        configure_firewall_rules()
    else:
        print("\nTo run the configuration, execute: python your_script_name.py run")
        
    #python3 iptables_firewall.py run
      #--- Configuring Firewall Rules ---
      # Success: iptables -A INPUT -s 192.168.1.0/24 -j DROP
      # Success: iptables -A INPUT -p tcp --dport 22 -j REJECT

      #--- Rules Applied ---
      #Run 'sudo iptables -L' to view the active rules.
      #sudo iptables -L INPUT --line-numbers
      #You should see your two new rules near the end of the list:
      #One rule blocking the source network 192.168.1.0/24.
      #One rule rejecting TCP traffic destined for port 22 (ssh).
      
        #The iptables tool works by examining packets against a series of rules organized into Chains (e.g., INPUT, OUTPUT, FORWARD).
        #-A INPUT: Appends the rule to the INPUT chain (for packets destined for the local system).
        #-s 192.168.1.0/24: Matches the source address/network. The /24 is CIDR notation for a Class C network, indicating the first 24 bits are fixed.
        #-p tcp --dport 22: Matches the protocol (TCP) and the destination port (22).
        #-j DROP: The Jump target/action. DROP means the packet is discarded silently.
        #-j REJECT: The Jump target/action. REJECT discards the packet but sends an error notification back to the sender.
        
        