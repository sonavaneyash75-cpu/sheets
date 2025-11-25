# client.py
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Configuration
HOST = '127.0.0.1'
PORT = 65432

def encrypt_message(message, key_data):
    """Encrypts a message using the server's public key."""
    rsa_public_key = RSA.import_key(key_data)
    cipher_rsa = PKCS1_OAEP.new(rsa_public_key)
    # RSA encryption works on bytes
    encrypted_message = cipher_rsa.encrypt(message.encode('utf-8'))
    return encrypted_message

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Connection refused. Ensure the server is running.")
        exit()
        
    print(f"Connected to server on {HOST}:{PORT}")

    # 1. Receive Public Key from Server
    server_public_key = s.recv(2048) # Enough to receive the 2048-bit key
    print("Received server's public key.")
    
    # 2. Encrypt and Send Message
    message_to_send = input("Enter message to send: ")
    
    encrypted_data = encrypt_message(message_to_send, server_public_key)
    print(f"Sending encrypted data ({len(encrypted_data)} bytes).")
    s.sendall(encrypted_data)
    
    # 3. Receive Acknowledgment
    acknowledgement = s.recv(1024).decode('utf-8')
    print(f"Server Response: {acknowledgement}")