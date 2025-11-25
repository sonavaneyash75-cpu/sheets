import math

def extended_gcd(a, b):
    """
    Implements the Extended Euclidean Algorithm.
    Returns a tuple (g, x, y) such that a*x + b*y = g = gcd(a, b).
    """
    if a == 0:
        return (b, 0, 1)
    
    g, x1, y1 = extended_gcd(b % a, a)
    
    # Update x and y using the results from the recursive call
    x = y1 - (b // a) * x1
    y = x1
    
    return (g, x, y)

def mod_inverse(a, m):
    """
    Finds the modular multiplicative inverse a^-1 mod m.
    Returns -1 if the inverse does not exist.
    """
    g, x, y = extended_gcd(a, m)
    
    if g != 1:
        # Modular inverse exists only if gcd(a, m) = 1
        raise ValueError("Modular inverse does not exist (a and m are not coprime)")
    
    # Ensure the result is positive and in the range [0, m-1]
    return x % m

def chinese_remainder_theorem(num, rem):
    """
    Solves the system of congruences:
    x = rem[i] (mod num[i])
    where num[i] are the moduli and rem[i] are the remainders.
    """
    # 1. Calculate the product M of all moduli (N in the formula)
    M = 1
    for n in num:
        M *= n
        
    # 2. Compute the solution x
    result = 0
    for n_i, r_i in zip(num, rem):
        
        # M_i = M / n_i
        M_i = M // n_i
        
        # M_i_inv = M_i^-1 mod n_i (Modular Inverse)
        M_i_inv = mod_inverse(M_i, n_i)
        
        # Term to add: r_i * M_i * M_i_inv
        term = r_i * M_i * M_i_inv
        
        result = (result + term) % M

    return result

def run_crt_menu():
    """
    Menu-driven function to gather inputs and solve the CRT.
    """
    print("\n--- Chinese Remainder Theorem Solver (Python) ---")
    
    try:
        k = int(input("Enter the number of congruences (k): "))
        if k <= 0:
            print("Invalid input for k. Must be positive.")
            return

        num = []
        rem = []
        print("Enter the system of congruences x = rem[i] (mod num[i]):")
        for i in range(k):
            print(f"\nCongruence {i + 1} (x = r (mod n)):")
            
            # Use raw input and convert
            r_i = int(input(f"  Enter remainder r[{i + 1}]: "))
            n_i = int(input(f"  Enter modulus n[{i + 1}]: "))

            if n_i <= 0:
                print("Modulus must be positive.")
                return

            num.append(n_i)
            rem.append(r_i)

        # Quick check for pairwise coprimality (not strictly necessary for the code to run, 
        # but CRT assumes it for a unique solution).
        for i in range(k):
            for j in range(i + 1, k):
                if math.gcd(num[i], num[j]) != 1:
                    print("\n Warning: The moduli are not pairwise coprime.")
                    print("The standard CRT guarantees a unique solution only for coprime moduli.")
                    # We proceed with the calculation anyway, which solves the general system of congruences

        solution = chinese_remainder_theorem(num, rem)
        M = 1
        for n in num:
            M *= n

        print("\n Solution Found")
        print(f"The smallest non-negative solution x is: {solution}")
        print(f"The general solution is x \u2261 {solution} (mod {M})")

    except ValueError as e:
        print(f"\nError: Invalid input. Please ensure all values are integers. ({e})")
    except Exception as e:
        print(f"\nAn error occurred during calculation: {e}")


# Main menu loop
def main():
    while True:
        print("\n\n=== CRT Menu (Python) ===")
        print("1. Solve Chinese Remainder Theorem")
        print("2. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            run_crt_menu()
        elif choice == '2':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()