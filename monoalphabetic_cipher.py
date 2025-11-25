import string

# Define the standard alphabet (used for reference)
STANDARD_ALPHABET = string.ascii_uppercase
# Define a default key (a sample substitution alphabet)
# The key is a permutation of the standard alphabet.
# Using 'X' for 'A', 'N' for 'B', etc.
DEFAULT_KEY = "XNBYHOCZTDJVSKGMELWRAPQIFU"

def get_cipher_key():
    """Returns the substitution key used for the cipher."""
    # In a real-world scenario, you might prompt the user for a custom key
    # or generate a random one. For this example, we use a fixed default.
    return DEFAULT_KEY

def encrypt_monoalphabetic(plaintext, key):
    """
    Encrypts the plaintext using the Monoalphabetic Substitution Cipher.

    :param plaintext: The original message (string).
    :param key: The 26-character substitution alphabet (string).
    :return: The encrypted ciphertext (string).
    """
    # 1. Map the STANDARD_ALPHABET to the KEY
    # The translation table maps: A->X, B->N, C->B, etc.
    translation_table = str.maketrans(STANDARD_ALPHABET, key)

    # 2. Convert the plaintext to uppercase to handle all letters uniformly
    uppercase_plaintext = plaintext.upper()

    # 3. Translate the uppercase plaintext
    ciphertext = uppercase_plaintext.translate(translation_table)

    # Note: Non-alphabetic characters (spaces, punctuation) are preserved
    # because they are not in the STANDARD_ALPHABET.
    return ciphertext

def decrypt_monoalphabetic(ciphertext, key):
    """
    Decrypts the ciphertext using the Monoalphabetic Substitution Cipher.

    :param ciphertext: The encrypted message (string).
    :param key: The 26-character substitution alphabet (string).
    :return: The original plaintext (string).
    """
    # 1. Map the KEY back to the STANDARD_ALPHABET for decryption
    # The inverse translation table maps: X->A, N->B, B->C, etc.
    # The decryption map is KEY -> STANDARD_ALPHABET
    inverse_translation_table = str.maketrans(key, STANDARD_ALPHABET)

    # 2. Convert the ciphertext to uppercase for uniform handling
    uppercase_ciphertext = ciphertext.upper()

    # 3. Translate the uppercase ciphertext
    plaintext = uppercase_ciphertext.translate(inverse_translation_table)

    return plaintext

def main():
    """Main menu-driven program loop."""
    print("--- 🔒 Monoalphabetic Substitution Cipher Program ---")
    key = get_cipher_key()
    print(f"**Current Substitution Key:** {key}")
    print(f"**Standard Alphabet:** {STANDARD_ALPHABET}\n")

    while True:
        print("\n--- Menu ---")
        print("1. **Encrypt** a message")
        print("2. **Decrypt** a message")
        print("3. **Exit**")
        
        choice = input("Enter your choice (1, 2, or 3): ").strip()
        
        if choice == '1':
            # --- ENCRYPTION ---
            plaintext = input("Enter the message to **encrypt**: ")
            ciphertext = encrypt_monoalphabetic(plaintext, key)
            print(f"\n✅ **Ciphertext:** {ciphertext}")
            
        elif choice == '2':
            # --- DECRYPTION ---
            ciphertext = input("Enter the message to **decrypt**: ")
            # Decryption handles non-letters from encryption as well
            decrypted_text = decrypt_monoalphabetic(ciphertext, key)
            print(f"\n✅ **Decrypted Plaintext:** {decrypted_text}")
            
        elif choice == '3':
            # --- EXIT ---
            print("\n👋 Exiting the program. Goodbye!")
            break
            
        else:
            print("\n❌ Invalid choice. Please enter 1, 2, or 3.")
            
# Execute the main function
if __name__ == "__main__":
    main()

#