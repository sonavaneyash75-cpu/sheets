import string

# --- Configuration ---
KEY_SQUARE_SIZE = 5
STANDARD_ALPHABET = string.ascii_uppercase.replace('J', '') # Use I/J rule

def create_key_square(key):
    """
    Creates the 5x5 Playfair key square (matrix).
    J is typically omitted, with I and J treated as the same character ('I').
    """
    key = key.upper().replace('J', 'I')
    key_chars = []
    
    # 1. Add unique characters from the key
    for char in key:
        if char not in key_chars and char in STANDARD_ALPHABET:
            key_chars.append(char)
            
    # 2. Add remaining characters from the standard alphabet
    for char in STANDARD_ALPHABET:
        if char not in key_chars:
            key_chars.append(char)
            
    # 3. Create the 5x5 matrix
    key_square = []
    for i in range(KEY_SQUARE_SIZE):
        key_square.append(key_chars[i * KEY_SQUARE_SIZE : (i + 1) * KEY_SQUARE_SIZE])
        
    return key_square

def find_position(key_square, char):
    """
    Finds the row and column (r, c) of a character in the key square.
    """
    # Handle the I/J rule: always search for 'I' if 'J' is passed
    if char == 'J':
        char = 'I'
        
    for r in range(KEY_SQUARE_SIZE):
        for c in range(KEY_SQUARE_SIZE):
            if key_square[r][c] == char:
                return r, c
    return None # Should not happen for valid characters

def preprocess_plaintext(plaintext):
    """
    Cleans plaintext, applies the I/J rule, and prepares it for digraphs:
    1. Converts to uppercase.
    2. Removes non-alphabetic characters.
    3. Replaces J with I.
    4. Inserts filler ('X') if two adjacent letters are the same.
    5. Appends filler ('X') if the total length is odd.
    """
    
    # 1, 2, 3: Clean and standardize
    text = plaintext.upper()
    text = ''.join(c for c in text if 'A' <= c <= 'Z')
    text = text.replace('J', 'I')
    
    # 4. Insert filler 'X' for double letters
    i = 0
    while i < len(text) - 1:
        if text[i] == text[i+1]:
            text = text[:i+1] + 'X' + text[i+1:]
        i += 2
        
    # 5. Append filler 'X' if length is odd
    if len(text) % 2 != 0:
        text += 'X'
        
    return [text[i:i+2] for i in range(0, len(text), 2)] # Return list of digraphs

def playfair_process(digraphs, key_square, mode='encrypt'):
    """
    Performs the core Playfair substitution (encryption or decryption).
    """
    processed_text = []
    
    # Determine the shift direction (+1 for encrypt, -1 for decrypt)
    shift = 1 if mode == 'encrypt' else -1

    for L1, L2 in digraphs:
        r1, c1 = find_position(key_square, L1)
        r2, c2 = find_position(key_square, L2)

        # Rule 1: Same Row
        if r1 == r2:
            new_L1 = key_square[r1][(c1 + shift) % KEY_SQUARE_SIZE]
            new_L2 = key_square[r2][(c2 + shift) % KEY_SQUARE_SIZE]
            
        # Rule 2: Same Column
        elif c1 == c2:
            new_L1 = key_square[(r1 + shift) % KEY_SQUARE_SIZE][c1]
            new_L2 = key_square[(r2 + shift) % KEY_SQUARE_SIZE][c2]
            
        # Rule 3: Rectangle
        else:
            # Swap column indices
            new_L1 = key_square[r1][c2]
            new_L2 = key_square[r2][c1]
        
        processed_text.append(new_L1 + new_L2)

    return "".join(processed_text)

def main():
    """Main menu-driven program loop."""
    print("--- 🔒 Playfair Cipher Program ---")
    
    # --- Key Setup ---
    while True:
        key = input("Enter the encryption key (a word or phrase): ").strip()
        if key:
            break
        print("Key cannot be empty.")
        
    key_square = create_key_square(key)
    
    print("\n**Generated 5x5 Key Square:**")
    # Display the key square nicely
    print('  ' + ' '.join(str(i) for i in range(KEY_SQUARE_SIZE)))
    for r in range(KEY_SQUARE_SIZE):
        print(f'{r} ' + ' '.join(key_square[r]))
    
    

    while True:
        print("\n--- Menu ---")
        print("1. **Encrypt** a message")
        print("2. **Decrypt** a message")
        print("3. **Exit**")
        
        choice = input("Enter your choice (1, 2, or 3): ").strip()
        
        if choice == '1':
            # --- ENCRYPTION ---
            plaintext = input("Enter the message to **encrypt**: ")
            digraphs = preprocess_plaintext(plaintext)
            ciphertext = playfair_process(digraphs, key_square, mode='encrypt')
            
            print(f"\n   **Preprocessed Digraphs:** {' '.join(digraphs)}")
            print(f"✅ **Ciphertext:** {ciphertext}")
            
        elif choice == '2':
            # --- DECRYPTION ---
            ciphertext = input("Enter the message to **decrypt**: ")
            
            # Decryption only needs cleaning (uppercase, remove non-alpha, I/J rule)
            cleaned_ciphertext = ciphertext.upper().replace('J', 'I')
            cleaned_ciphertext = ''.join(c for c in cleaned_ciphertext if 'A' <= c <= 'Z')
            
            # Group into digraphs (must be even length for proper Playfair cipher text)
            if len(cleaned_ciphertext) % 2 != 0:
                 print("\n❌ Error: Ciphertext length is odd. Cannot decrypt.")
                 continue
                 
            digraphs = [cleaned_ciphertext[i:i+2] for i in range(0, len(cleaned_ciphertext), 2)]
            
            decrypted_text = playfair_process(digraphs, key_square, mode='decrypt')
            
            print(f"\n✅ **Decrypted Plaintext:** {decrypted_text}")
            
        elif choice == '3':
            # --- EXIT ---
            print("\n👋 Exiting the Playfair program. Goodbye!")
            break
            
        else:
            print("\n❌ Invalid choice. Please enter 1, 2, or 3.")
            
# Execute the main function
if __name__ == "__main__":
    main()