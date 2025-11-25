import socket
import random

# --- Diffie-Hellman Functions ---

def generate_params():
    # In a real-world scenario, 'p' would be a very large safe prime
    # and 'g' a primitive root modulo 'p'.
    # We use small values for demonstration.
    P = 23  # A large prime number (p)
    G = 5   # A base or generator (g)
    return P, G

def calculate_public_key(g, private_key, p):
    # Public Key = (g ^ private_key) mod p
    return pow(g, private_key, p)

def calculate_shared_secret(public_key, private_key, p):
    # Shared Secret = (other_party_public_key ^ my_private_key) mod p
    return pow(public_key, private_key, p)

# --- Socket Setup ---
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}...")
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")

        # 1. Generate DH parameters
        P, G = generate_params()
        print(f"\n[SERVER] 1. Using Public Parameters: P={P}, G={G}")

        # 2. Generate Server's Private Key 'a'
        # Private key 'a' must be 1 < a < P
        private_key_a = random.randint(2, P - 1)
        print(f"[SERVER] 2. My Private Key (a): {private_key_a}")

        # 3. Calculate Server's Public Key 'A'
        public_key_A = calculate_public_key(G, private_key_a, P)
        print(f"[SERVER] 3. My Public Key (A): {public_key_A}")
        
        # 4. Send P, G, and Server's Public Key A to Client
        data_to_send = f"{P},{G},{public_key_A}"
        conn.sendall(data_to_send.encode())
        print(f"[SERVER] 4. Sent P, G, and A to client.")

        # 5. Receive Client's Public Key 'B'
        data = conn.recv(1024).decode()
        if data:
            public_key_B = int(data)
            print(f"[SERVER] 5. Received Client's Public Key (B): {public_key_B}")

            # 6. Calculate Shared Secret Key 'S'
            shared_secret = calculate_shared_secret(public_key_B, private_key_a, P)
            print("-" * 40)
            print(f" [SERVER] Shared Secret Key Calculated: {shared_secret}")
            print("-" * 40)
        else:
            print("[SERVER] Connection closed by client before key exchange was complete.")