#pip install pycryptodome

# server.py
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Configuration
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# 1. Generate RSA Key Pair
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

print("Server generated keys.")

def decrypt_message(encrypted_data):
    """Decrypts data using the server's private key."""
    rsa_key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    try:
        decrypted_message = cipher_rsa.decrypt(encrypted_data).decode('utf-8')
        return decrypted_message
    except ValueError as e:
        print(f"Decryption Error: {e}")
        return None

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}...")
    
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        
        # 2. Send Public Key to Client
        print("Sending public key to client...")
        conn.sendall(public_key)

        # 3. Receive and Decrypt Messages
        while True:
            # We must receive a known length or use a prefixed length for large data
            encrypted_msg_bytes = conn.recv(256) # RSA-2048 output size is 256 bytes
            if not encrypted_msg_bytes:
                break
            
            print(f"Received encrypted data ({len(encrypted_msg_bytes)} bytes).")
            
            decrypted_msg = decrypt_message(encrypted_msg_bytes)
            
            if decrypted_msg:
                print(f"Decrypted Message: **{decrypted_msg}**")
            else:
                print("Failed to decrypt message.")
            
            # Send an acknowledgement back
            conn.sendall(b"Server acknowledged receipt.")