def encrypt_rail_fence(text, rails):
    """Stage 1: Standard Rail Fence Transposition (Zig-Zag)"""
    n = len(text)
    grid = [['' for _ in range(n)] for _ in range(rails)]
    r, c, down = 0, 0, True
    
    # 1. Fill the Grid
    for char in text:
        grid[r][c] = char
        c += 1
        if r == 0: down = True
        elif r == rails - 1: down = False
        r += 1 if down else -1
        
    # 2. Read Row by Row for Intermediate Ciphertext
    intermediate = ""
    for r in range(rails):
        for c in range(n):
            if grid[r][c] != '':
                intermediate += grid[r][c]
    return intermediate

def encrypt_double(plaintext, rails):
    """Double Rail Fence Encryption (Rail Fence -> Columnar)"""
    # Stage 1: Rail Fence
    intermediate = encrypt_rail_fence(plaintext, rails)
    
    # Stage 2: Simplified Columnar Transposition (Read Cyclically)
    blocks = ['' for _ in range(rails)]
    for i, char in enumerate(intermediate):
        blocks[i % rails] += char
        
    return "".join(blocks)

def decrypt_double(ciphertext, rails):
    """Double Rail Fence Decryption (Reverse Columnar -> Reverse Rail Fence)"""
    n = len(ciphertext)
    
    # Stage 1: Reverse Columnar (Reconstruct Intermediate Text)
    
    # Calculate block lengths for splitting
    base_len = n // rails
    remainder = n % rails
    col_lengths = [base_len + 1] * remainder + [base_len] * (rails - remainder)
    
    # Split the ciphertext into blocks
    blocks = []
    start = 0
    for length in col_lengths:
        blocks.append(ciphertext[start:start + length])
        start += length
        
    # Reconstruct intermediate text by reading across blocks
    intermediate = [''] * n
    block_indices = [0] * rails
    for i in range(n):
        block_idx = i % rails
        intermediate[i] = blocks[block_idx][block_indices[block_idx]]
        block_indices[block_idx] += 1
        
    intermediate = "".join(intermediate)
    
    # Stage 2: Reverse Rail Fence (Un-Zig-Zag)
    
    # Map the positions of characters ('*')
    grid_pos = [['\n' for _ in range(n)] for _ in range(rails)]
    r, c, down = 0, 0, True
    for _ in range(n):
        grid_pos[r][c] = '*'
        c += 1
        if r == 0: down = True
        elif r == rails - 1: down = False
        r += 1 if down else -1
        
    # Populate the marked positions with the intermediate text (Row-by-Row)
    idx = 0
    for r in range(rails):
        for c in range(n):
            if grid_pos[r][c] == '*':
                grid_pos[r][c] = intermediate[idx]
                idx += 1
                
    # Read the final plaintext by following the zig-zag path
    final_plaintext = []
    r, c, down = 0, 0, True
    for _ in range(n):
        final_plaintext.append(grid_pos[r][c])
        c += 1
        if r == 0: down = True
        elif r == rails - 1: down = False
        r += 1 if down else -1
            
    return "".join(final_plaintext)

# ----------------- EXECUTION -----------------
# NOTE: Use simple, uppercase text without spaces for quick testing.
# Example: "TRANSPORTATION" with 4 rails.

# User Input (Keep it simple and assume valid input)
plaintext = input("Enter plaintext (e.g., NODELAYATALL): ").upper().replace(" ", "")
try:
    rails = int(input("Enter number of rails (e.g., 3 or 4): "))
except ValueError:
    print("Invalid rails count. Exiting.")
    rails = 0
    
if rails >= 2 and rails < len(plaintext):
    # Encrypt
    ciphertext = encrypt_double(plaintext, rails)
    print(f"\nEncrypted Ciphertext: {ciphertext}")

    # Decrypt
    decrypted_text = decrypt_double(ciphertext, rails)
    print(f"Decrypted Plaintext:  {decrypted_text}")

    # Verify
    print(f"\nVerification: {plaintext == decrypted_text}")
else:
    print("Error: Rails must be between 2 and text length - 1.")
