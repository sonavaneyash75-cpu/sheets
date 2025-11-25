import math

def double_rail_fence_encrypt(plaintext: str, rails: int) -> str:
    """
    Encrypts the plaintext using the Double Row Column Rail Fence cipher.

    Args:
        plaintext: The message to encrypt (uppercase and without spaces recommended).
        rails: The number of rails (rows) for the first stage.

    Returns:
        The resulting ciphertext.
    """
    n = len(plaintext)
    
    # 1. Standard Rail Fence Transposition (Rows)
    
    grid = [['' for _ in range(n)] for _ in range(rails)]
    
    row, col = 0, 0
    direction_down = True
    
    for char in plaintext:
        grid[row][col] = char
        col += 1
        
        if row == 0:
            direction_down = True
        elif row == rails - 1:
            direction_down = False
            
        if direction_down:
            row += 1
        else:
            row -= 1

    # Read the grid row by row to get the intermediate ciphertext
    intermediate_ciphertext = []
    for r in range(rails):
        for c in range(n):
            if grid[r][c] != '':
                intermediate_ciphertext.append(grid[r][c])
                
    # 2. Columnar Transposition (Simplified block-based read)
    
    final_ciphertext_blocks = ['' for _ in range(rails)]
    
    for i, char in enumerate(intermediate_ciphertext):
        block_index = i % rails
        final_ciphertext_blocks[block_index] += char
        
    return "".join(final_ciphertext_blocks)


def double_rail_fence_decrypt(ciphertext: str, rails: int) -> str:
    """
    Decrypts the ciphertext using the Double Row Column Rail Fence cipher.

    Args:
        ciphertext: The message to decrypt.
        rails: The number of rails (rows) for the first stage.

    Returns:
        The resulting plaintext.
    """
    n = len(ciphertext)
    
    # 1. Reverse Columnar Transposition
    
    base_len = n // rails
    remainder = n % rails
    
    col_lengths = [base_len + 1] * remainder + [base_len] * (rails - remainder)
    
    blocks = []
    start_index = 0
    for length in col_lengths:
        blocks.append(ciphertext[start_index:start_index + length])
        start_index += length
        
    intermediate_plaintext = [''] * n
    block_indices = [0] * rails
    
    for i in range(n):
        block_index = i % rails
        
        char = blocks[block_index][block_indices[block_index]]
        intermediate_plaintext[i] = char
        
        block_indices[block_index] += 1
        
    intermediate_plaintext = "".join(intermediate_plaintext)
    
    # 2. Reverse Standard Rail Fence Transposition (Rows)
    
    grid_pos = [['\n' for _ in range(n)] for _ in range(rails)]
    
    row, col = 0, 0
    direction_down = True
    
    for i in range(n):
        grid_pos[row][col] = '*'
        col += 1
        
        if row == 0:
            direction_down = True
        elif row == rails - 1:
            direction_down = False
            
        if direction_down:
            row += 1
        else:
            row -= 1

    index = 0
    for r in range(rails):
        for c in range(n):
            if grid_pos[r][c] == '*':
                grid_pos[r][c] = intermediate_plaintext[index]
                index += 1
                
    final_plaintext = []
    row, col = 0, 0
    direction_down = True
    
    for i in range(n):
        final_plaintext.append(grid_pos[row][col])
        col += 1
        
        if row == 0:
            direction_down = True
        elif row == rails - 1:
            direction_down = False
            
        if direction_down:
            row += 1
        else:
            row -= 1
            
    return "".join(final_plaintext)

# --- User Input and Execution ---

if __name__ == "__main__":
    print("--- Double Row Column Rail Fence Cipher ---")

    # Get plaintext input from the user
    user_plaintext = input("Enter the message (use UPPECASE and underscores/no spaces for best results): ").upper()
    
    # Get rails input from the user with input validation
    while True:
        try:
            user_rails = int(input("Enter the number of rails (e.g., 3, 4, 5): "))
            if user_rails < 2 or user_rails >= len(user_plaintext):
                print(f"Please enter a number of rails between 2 and {len(user_plaintext) - 1}.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter an integer for the number of rails.")

    # 1. Encryption
    ciphertext = double_rail_fence_encrypt(user_plaintext, user_rails)
    print("\n ENCRYPTION RESULT ")
    print(f"Original Plaintext:   {user_plaintext}")
    print(f"Number of Rails:      {user_rails}")
    print(f"Encrypted Ciphertext: {ciphertext}")

    # 2. Decryption
    decrypted_text = double_rail_fence_decrypt(ciphertext, user_rails)
    print("\n DECRYPTION RESULT ")
    print(f"Ciphertext:           {ciphertext}")
    print(f"Decrypted Plaintext:  {decrypted_text}")

    # 3. Verification
    print("\n Verification:")
    if user_plaintext == decrypted_text:
        print("Decryption successful: Plaintext matches original message.")
    else:
        print("Decryption failed: Plaintext DOES NOT match original message.")