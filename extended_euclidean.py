# Function to perform the Extended Euclidean Algorithm (EEA).
# It finds integers x and y such that s*x + t*y = gcd(s, t).
def extended_euclidean(s, t):
    # Base case of the recursion.
    # If the first number (s) is 0, the GCD is the second number (t).
    # The equation becomes: t*0 + t*1 = t
    if s == 0:
        # Return: (gcd, x, y) -> (t, 0, 1)
        return t, 0, 1
    
    # Recursive step: Apply the algorithm to (t % s) and s.
    # The coefficients (x1, y1) returned satisfy: (t % s)*x1 + s*y1 = gcd(s, t)
    g, x1, y1 = extended_euclidean(t % s, s)

    # Use the identity t % s = t - (t // s) * s to find the new x and y.
    # Substitute the identity into the previous equation and rearrange terms:
    # (t - (t // s) * s) * x1 + s * y1 = g
    # s * (y1 - (t // s) * x1) + t * x1 = g
    
    # The new coefficient for s (x) is: y1 - (t // s) * x1
    x = y1 - (t // s) * x1
    # The new coefficient for t (y) is: x1
    y = x1

    # Return the GCD and the current coefficients (x, y)
    return g, x, y

# Function to find the Multiplicative Inverse of 'a' modulo 'm'.
# Returns the inverse (0 <= inverse < m) or -1 if no inverse exists.
def multiplicative_inverse(a, m):
    # Step 1: Ensure 'a' is within the range [0, m-1]
    a = a % m
    if a < 0:
        a += m

    # Step 2: Run the Extended Euclidean Algorithm
    # We are looking for x such that a*x + m*y = gcd(a, m)
    g, x, y = extended_euclidean(a, m)
    
    # Step 3: Check if the inverse exists
    if g != 1:
        # The inverse exists ONLY if gcd(a, m) is 1 (a and m are coprime).
        return -1
    else:
        # Step 4: Adjust the coefficient 'x'
        # 'x' is the inverse, but it might be negative.
        # x % m ensures the result is in the range [0, m-1].
        return x % m

# --- Main Program Execution Block ---
if __name__ == "__main__":
    print("\n--- Extended Euclidean Algorithm (EEA) and Multiplicative Inverse ---")
    
    # --- Part 1: EEA Demonstration ---
    try:
        print("\n[PART 1: Find GCD and Bézout's Coefficients (s*x + t*y = gcd)]")
        s = int(input("Enter the first number (s): "))
        t = int(input("Enter the second number (t): "))
        
        # Call the EEA function
        g, x, y = extended_euclidean(s, t)
        
        # Display the results
        print(f"\nEEA Results for gcd({s}, {t}):")
        print(f"Greatest Common Divisor (gcd) = {g}")
        print(f"Bézout's Coefficients: x = {x}, y = {y}")
        # Verification: Check if s*x + t*y equals g
        print(f"Verification: {s}*{x} + {t}*{y} = {s*x + t*y} (Target: {g})")
        
    except ValueError:
        print("Invalid input. Please enter valid integers for s and t.")
        
    # --- Part 2: Multiplicative Inverse Demonstration ---
    try:
        print("\n" + "-"*50)
        print("[PART 2: Find Multiplicative Inverse (a*x = 1 mod m)]")
        a = int(input("Enter the number (a) for the inverse: "))
        m = int(input("Enter the modulus (m): "))
        
        # Call the MI function
        inv = multiplicative_inverse(a, m)
        
        # Display MI results
        print(f"\nMI Results for {a} mod {m}:")
        if inv != -1:
            print(f"Multiplicative Inverse is: {inv}")
            # Verification: Check if a * inv is congruent to 1 mod m
            print(f"Verification: {a}*{inv} mod {m} = {(a * inv) % m} (Target: 1)")
        else:
            print(f"Inverse does NOT exist because gcd({a}, {m}) != 1.")
            
    except ValueError:
        print("Invalid input. Please enter valid integers for a and m.")