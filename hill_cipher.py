import numpy as np
import string

# --- Configuration ---
ALPHABET_SIZE = 26
STANDARD_ALPHABET = string.ascii_uppercase

# Mapping: A=0, B=1, ..., Z=25
char_to_int = {c: i for i, c in enumerate(STANDARD_ALPHABET)}
int_to_char = {i: c for i, c in enumerate(STANDARD_ALPHABET)}

def inverse_matrix_mod_26(matrix):
    """
    Calculates the inverse of a matrix modulo 26.
    This is the most complex part of the Hill Cipher.
    """
    det = int(round(np.linalg.det(matrix)))
    # Ensure determinant is positive
    det = det % ALPHABET_SIZE
    
    # 1. Check if the modular inverse of the determinant exists (GCD must be 1)
    # The modular inverse of 'det' modulo 26 is 'det_inv'.
    det_inv = -1
    for i in range(ALPHABET_SIZE):
        if (det * i) % ALPHABET_SIZE == 1:
            det_inv = i
            break
            
    if det_inv == -1:
        # Cannot be decrypted if the key is not invertible mod 26
        raise ValueError(f"Key is not invertible (det={det}, GCD(det, 26) != 1). Choose a different key.")
        
    # 2. Calculate the matrix of cofactors, transpose it (adjugate)
    adjugate = np.linalg.inv(matrix) * np.linalg.det(matrix)
    # Rounding is crucial for floating point results
    adjugate = np.round(adjugate).astype(int)
    
    # 3. Calculate the inverse matrix: adjugate * det_inv (mod 26)
    inverse = (adjugate * det_inv) % ALPHABET_SIZE
    
    return inverse

def preprocess_text(text, key_size, fill_char='X'):
    """
    Cleans plaintext and pads it to match the key matrix size.
    """
    # 1. Clean and convert to uppercase
    text = text.upper()
    text = ''.join(c for c in text if 'A' <= c <= 'Z')
    
    # 2. Pad with a filler character ('X') if length is not a multiple of key_size
    while len(text) % key_size != 0:
        text += fill_char
        
    return text

def encrypt_hill(plaintext, key_matrix):
    """
    Encrypts the plaintext using the Hill Cipher: C = P * K (mod 26).
    """
    key_size = key_matrix.shape[0]
    processed_text = preprocess_text(plaintext, key_size)
    
    # Convert text to numerical vector blocks
    P_blocks = [
        [char_to_int[processed_text[i + j]] for j in range(key_size)] 
        for i in range(0, len(processed_text), key_size)
    ]
    
    ciphertext = []
    
    for P in P_blocks:
        P_vector = np.array(P)
        
        # Matrix multiplication: C = P * K (mod 26)
        # Result is a 1xN vector
        C_vector = np.dot(P_vector, key_matrix) % ALPHABET_SIZE
        
        # Convert numerical result back to characters
        ciphertext.extend([int_to_char[c] for c in C_vector])
        
    return "".join(ciphertext)

def decrypt_hill(ciphertext, key_matrix):
    """
    Decrypts the ciphertext using the Hill Cipher: P = C * K_inv (mod 26).
    """
    try:
        # Calculate the inverse of the key matrix mod 26
        inverse_key = inverse_matrix_mod_26(key_matrix)
    except ValueError as e:
        return f"DECRYPTION FAILED: {e}"

    key_size = key_matrix.shape[0]
    
    # Decryption works on the raw ciphertext (must be multiple of key_size)
    if len(ciphertext) % key_size != 0:
         return "DECRYPTION FAILED: Ciphertext length must be a multiple of the key size."
         
    # Convert text to numerical vector blocks
    C_blocks = [
        [char_to_int[ciphertext[i + j]] for j in range(key_size)] 
        for i in range(0, len(ciphertext), key_size)
    ]
    
    plaintext = []
    
    for C in C_blocks:
        C_vector = np.array(C)
        
        # Matrix multiplication: P = C * K_inv (mod 26)
        P_vector = np.dot(C_vector, inverse_key) % ALPHABET_SIZE
        
        # Convert numerical result back to characters
        plaintext.extend([int_to_char[p] for p in P_vector])
        
    return "".join(plaintext)

def get_key_matrix():
    """Prompts user for the key matrix (2x2 or 3x3)."""
    while True:
        try:
            size = int(input("Enter the key size (N for NxN matrix, e.g., 2 or 3): "))
            if size <= 1 or size > 4:
                 print("Key size must be 2, 3, or 4.")
                 continue
                 
            print(f"Enter the {size*size} elements of the key matrix (row by row), separated by spaces:")
            elements = input(f"e.g., for 2x2: 17 17 5 21\n> ").split()
            
            if len(elements) != size * size:
                print(f"Must enter exactly {size*size} numbers.")
                continue
                
            matrix_elements = [int(e) for e in elements]
            key_matrix = np.array(matrix_elements).reshape(size, size)
            
            # Test invertibility immediately
            det = int(round(np.linalg.det(key_matrix))) % ALPHABET_SIZE
            
            if np.gcd(det, ALPHABET_SIZE) != 1:
                print(f"\n❌ WARNING: Determinant modulo 26 is {det}. GCD(det, 26) is not 1.")
                print("This key is NOT invertible and DECRYPTION will fail. Please choose a new key.")
                continue
                
            return key_matrix
            
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter numbers only.")

def main():
    """Main menu-driven program loop."""
    print("--- 🔢 Hill Cipher Program (Requires NumPy) ---")
    
    # --- Key Setup ---
    key_matrix = get_key_matrix()
    
    print("\n**Using Key Matrix (K):**")
    print(key_matrix)
    print(f"**Key Size (N):** {key_matrix.shape[0]}\n")
    
    while True:
        print("\n--- Menu ---")
        print("1. **Encrypt** a message")
        print("2. **Decrypt** a message")
        print("3. **Exit**")
        
        choice = input("Enter your choice (1, 2, or 3): ").strip()
        
        if choice == '1':
            # --- ENCRYPTION ---
            plaintext = input("Enter the message to **encrypt**: ")
            ciphertext = encrypt_hill(plaintext, key_matrix)
            
            print(f"\n   **Plaintext (Padded):** {preprocess_text(plaintext, key_matrix.shape[0])}")
            print(f"✅ **Ciphertext:** {ciphertext}")
            
        elif choice == '2':
            # --- DECRYPTION ---
            ciphertext = input("Enter the message to **decrypt**: ")
            decrypted_text = decrypt_hill(ciphertext.upper(), key_matrix)
            
            print(f"\n✅ **Decrypted Plaintext:** {decrypted_text}")
            
        elif choice == '3':
            # --- EXIT ---
            print("\n👋 Exiting the Hill Cipher program. Goodbye!")
            break
            
        else:
            print("\n❌ Invalid choice. Please enter 1, 2, or 3.")
            
# Execute the main function
if __name__ == "__main__":
    main()
    
    #pip install numpy