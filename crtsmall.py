import math

def extended_gcd(a, b):
    # Implements the Extended Euclidean Algorithm: a*x + b*y = gcd(a, b)
    # Returns (g, x, y)
    if a == 0:
        return (b, 0, 1)
    
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return (g, x, y)

def mod_inverse(a, m):
    # Finds a^-1 mod m
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        # Raises an error if inverse doesn't exist (moduli are not coprime)
        raise ValueError(f"Inverse of {a} mod {m} does not exist!")
    return x % m

def solve_crt(num, rem):
    """
    Solves the system x = rem[i] (mod num[i])
    num: list of moduli (n_i)
    rem: list of remainders (a_i)
    """
    # 1. Calculate N (Total Modulus)
    N = 1
    for n in num:
        N *= n
        
    # 2. Compute the result x
    result = 0
    for n_i, r_i in zip(num, rem):
        
        # M_i = N / n_i
        M_i = N // n_i
        
        # M_i_inv = M_i^-1 mod n_i
        M_i_inv = mod_inverse(M_i, n_i)
        
        # Add a_i * M_i * M_i_inv to the sum
        term = r_i * M_i * M_i_inv
        
        # Accumulate the result modulo N
        result = (result + term) % N

    return result, N

# --- Menu Driven Execution for Demonstration ---

def main():
    print("--- Simplified Chinese Remainder Theorem Solver ---")
    print("Example: x = 2 (mod 3), x = 3 (mod 5), x = 2 (mod 7)")
    
    try:
        # Hardcoding the example for quick execution
        # num = [3, 5, 7]
        # rem = [2, 3, 2]
        
        # User input for flexibility
        k = int(input("Enter number of congruences: "))
        num = []
        rem = []
        for i in range(k):
            r = int(input(f"Enter remainder r[{i+1}]: "))
            n = int(input(f"Enter modulus n[{i+1}]: "))
            if n <= 0: raise ValueError("Modulus must be positive.")
            if i > 0 and any(math.gcd(n, existing_n) != 1 for existing_n in num):
                 print("\n⚠️ Warning: Moduli must be coprime for unique solution.")
            num.append(n)
            rem.append(r)
            
        solution, total_modulus = solve_crt(num, rem)
        
        print("\n✅ Solution Found")
        print(f"The smallest positive solution x is: {solution}")
        print(f"General Solution: x ≡ {solution} (mod {total_modulus})")

    except ValueError as e:
        print(f"\nError: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
