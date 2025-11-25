import socket
import random

# --- Diffie-Hellman Functions ---
# Note: These functions are identical to the server's, but are included
# here for the client's own calculations.

def calculate_public_key(g, private_key, p):
    # Public Key = (g ^ private_key) mod p
    return pow(g, private_key, p)

def calculate_shared_secret(public_key, private_key, p):
    # Shared Secret = (other_party_public_key ^ my_private_key) mod p
    return pow(public_key, private_key, p)

# --- Socket Setup ---
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Could not connect to server. Ensure the server script is running.")
        exit()

    print(f"Client connected to {HOST}:{PORT}")

    # 1. Receive P, G, and Server's Public Key 'A'
    data = s.recv(1024).decode()
    if not data:
        print("[CLIENT] Server closed the connection.")
        exit()

    P, G, public_key_A_str = data.split(',')
    P = int(P)
    G = int(G)
    public_key_A = int(public_key_A_str)
    print(f"\n[CLIENT] 1. Received Public Parameters: P={P}, G={G}")
    print(f"[CLIENT] 1. Received Server's Public Key (A): {public_key_A}")

    # 2. Generate Client's Private Key 'b'
    # Private key 'b' must be 1 < b < P
    private_key_b = random.randint(2, P - 1)
    print(f"[CLIENT] 2. My Private Key (b): {private_key_b}")

    # 3. Calculate Client's Public Key 'B'
    public_key_B = calculate_public_key(G, private_key_b, P)
    print(f"[CLIENT] 3. My Public Key (B): {public_key_B}")

    # 4. Send Client's Public Key B to Server
    s.sendall(str(public_key_B).encode())
    print(f"[CLIENT] 4. Sent B to server.")

    # 5. Calculate Shared Secret Key 'S'
    shared_secret = calculate_shared_secret(public_key_A, private_key_b, P)
    print("-" * 40)
    print(f" [CLIENT] Shared Secret Key Calculated: {shared_secret}")
    print("-" * 40)