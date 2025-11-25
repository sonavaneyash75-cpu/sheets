import string

# --- Configuration ---
ALPHABET_SIZE = 26
STANDARD_ALPHABET = string.ascii_uppercase

# Mapping: A=0, B=1, ..., Z=25
char_to_int = {c: i for i, c in enumerate(STANDARD_ALPHABET)}
int_to_char = {i: c for i, c in enumerate(STANDARD_ALPHABET)}

def get_key_stream(plaintext, key):
    """
    Generates a key stream the same length as the cleaned plaintext
    by repeating the keyword. Non-alphabetic characters in plaintext
    are ignored when generating the stream index.
    """
    key = key.upper()
    key_length = len(key)
    key_stream = ""
    key_index = 0

    for char in plaintext.upper():
        if 'A' <= char <= 'Z':
            # Append the key character and move to the next key index (wrapping)
            key_stream += key[key_index % key_length]
            key_index += 1
        else:
            # Append a placeholder (or the original char) for non-letters
            # to keep alignment, though only letter indices are used in encryption logic
            key_stream += char 

    return key_stream

def vigenere_process(text, key_stream, mode='encrypt'):
    """
    Performs the Vigenère substitution (encryption or decryption).
    
    Encryption: C = (P + K) mod 26
    Decryption: P = (C - K) mod 26
    """
    processed_text = []
    
    # Determine the shift operation (+ for encrypt, - for decrypt)
    operation = 1 if mode == 'encrypt' else -1

    for p_char, k_char in zip(text.upper(), key_stream):
        if 'A' <= p_char <= 'Z':
            # 1. Convert characters to their integer values (P and K)
            p_val = char_to_int[p_char]
            k_val = char_to_int[k_char]
            
            # 2. Apply the Vigenère formula with modular arithmetic
            if mode == 'encrypt':
                # (P + K) mod 26
                result_val = (p_val + k_val) % ALPHABET_SIZE
            else:
                # (C - K) mod 26
                # Adding 26 before subtraction ensures the result is positive
                result_val = (p_val - k_val + ALPHABET_SIZE) % ALPHABET_SIZE
            
            # 3. Convert the resulting integer back to a character (C or P)
            processed_text.append(int_to_char[result_val])
        else:
            # Non-alphabetic characters (spaces, punctuation) are preserved
            processed_text.append(p_char)

    return "".join(processed_text)

def main():
    """Main menu-driven program loop."""
    print("--- 📝 Vigenère (Polyalphabetic) Cipher Program ---")
    
    # --- Key Setup ---
    while True:
        key = input("Enter the encryption **keyword** (e.g., LEMON): ").strip()
        if key.isalpha():
            break
        print("Key must contain only letters.")
        
    print(f"\n**Using Key:** {key.upper()}\n")

    while True:
        print("\n--- Menu ---")
        print("1. **Encrypt** a message")
        print("2. **Decrypt** a message")
        print("3. **Exit**")
        
        choice = input("Enter your choice (1, 2, or 3): ").strip()
        
        if choice == '1':
            # --- ENCRYPTION ---
            plaintext = input("Enter the message to **encrypt**: ")
            
            # Key stream generation is crucial: non-letters in plaintext are handled
            key_stream = get_key_stream(plaintext, key)
            ciphertext = vigenere_process(plaintext, key_stream, mode='encrypt')
            
            # Displaying the key stream over the plaintext
            print("\n   Plaintext:  ", ' '.join(c for c in plaintext.upper() if c.isalpha()))
            print("   Key Stream: ", ' '.join(key_stream[i] for i, c in enumerate(plaintext.upper()) if c.isalpha()))
            print(f"✅ **Ciphertext:** {ciphertext}")
            
        elif choice == '2':
            # --- DECRYPTION ---
            ciphertext = input("Enter the message to **decrypt**: ")
            
            # The key stream generated here must match the one used during encryption
            key_stream = get_key_stream(ciphertext, key)
            decrypted_text = vigenere_process(ciphertext, key_stream, mode='decrypt')
            
            print(f"\n✅ **Decrypted Plaintext:** {decrypted_text}")
            
        elif choice == '3':
            # --- EXIT ---
            print("\n👋 Exiting the Vigenère program. Goodbye!")
            break
            
        else:
            print("\n❌ Invalid choice. Please enter 1, 2, or 3.")
            
# Execute the main function
if __name__ == "__main__":
    main()