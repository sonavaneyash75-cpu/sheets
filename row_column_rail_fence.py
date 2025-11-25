import math

# --- ENCRYPTION FUNCTION ---

def row_column_rail_fence_encrypt(plaintext: str, rows: int) -> str:
    """
    Encrypts a plaintext message using the Row-Column Rail Fence cipher.
    Writes row-by-row, reads column-by-column.
    Pads with 'X' if necessary.
    """
    # Remove spaces and convert to uppercase for standard cipher operation
    plaintext_clean = plaintext.replace(" ", "").upper()
    L = len(plaintext_clean)
    
    # Calculate dimensions
    columns = math.ceil(L / rows)
    grid_size = rows * columns
    
    # Padding: Pad the plaintext with 'X' to fit the grid
    padding_needed = grid_size - L
    padded_plaintext = plaintext_clean + 'X' * padding_needed
    
    # 1. Initialize the grid (matrix)
    grid = [['' for _ in range(columns)] for _ in range(rows)]
    
    # 2. Transposition: Write the padded plaintext into the grid row by row
    for k in range(grid_size):
        r = k // columns
        c = k % columns
        grid[r][c] = padded_plaintext[k]
        
    # 3. Readout: Read the ciphertext column by column
    ciphertext = []
    for c in range(columns):
        for r in range(rows):
            ciphertext.append(grid[r][c])
            
    return "".join(ciphertext)

# --- DECRYPTION FUNCTION ---

def row_column_rail_fence_decrypt(ciphertext: str, rows: int, original_length: int) -> str:
    """
    Decrypts a ciphertext message using the Row-Column Rail Fence cipher.
    Writes column-by-column, reads row-by-row, then depads.
    """
    L_cipher = len(ciphertext)
    
    # Calculate dimensions
    columns = math.ceil(L_cipher / rows)
    
    # 1. Grid Formation: Initialize the grid and fill it column by column
    grid = [['' for _ in range(columns)] for _ in range(rows)]
    
    k = 0 # Index for the ciphertext
    # Fill the grid column by column
    for c in range(columns):
        for r in range(rows):
            if k < L_cipher:
                grid[r][c] = ciphertext[k]
                k += 1
                
    # 2. Readout: Read the padded plaintext row by row
    padded_plaintext = []
    for r in range(rows):
        for c in range(columns):
            padded_plaintext.append(grid[r][c])
            
    full_text = "".join(padded_plaintext)
    
    # 3. Depadding: Trim to the original length
    # Note: We return the text as uppercase since the encryption process converted it.
    plaintext = full_text[:original_length]
    
    return plaintext

# --- USER INPUT AND EXECUTION ---

if __name__ == "__main__":
    
    # Get user input for plaintext
    while True:
        user_plaintext = input("Enter the message (Plaintext): ")
        if user_plaintext.strip():
            break
        print("Message cannot be empty. Please try again.")

    # Get user input for key (rows)
    while True:
        try:
            user_rows = int(input("Enter the key (Number of Rows, must be an integer > 1): "))
            if user_rows > 1:
                break
            print("The number of rows must be an integer greater than 1.")
        except ValueError:
            print("Invalid input. Please enter a valid integer for the number of rows.")

    # --- Execution ---
    
    # Store the length of the *original* message before cleaning/padding
    original_length = len(user_plaintext.replace(" ", ""))
    
    print("\n" + "=" * 40)
    print("      ROW-COLUMN RAIL FENCE CIPHER")
    print("=" * 40)
    print(f"Original Text: {user_plaintext}")
    print(f"Key (Rows): {user_rows}")
    print(f"Cleaned Length (for Decryption): {original_length}")
    print("-" * 40)
    
    # 1. ENCRYPT
    ciphertext = row_column_rail_fence_encrypt(user_plaintext, user_rows)
    print(f"Ciphertext: {ciphertext}")
    print("-" * 40)
    
    # 2. DECRYPT
    decrypted_text = row_column_rail_fence_decrypt(ciphertext, user_rows, original_length)
    print(f"Decrypted Text: {decrypted_text}")
    print("=" * 40)