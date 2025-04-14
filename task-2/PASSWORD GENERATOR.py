import random
import string

def generate_password(length, use_lower=True, use_upper=True, use_digits=True, use_special=True):
    """Generate password based on user-specified complexity"""
    character_sets = {
        'lower': string.ascii_lowercase if use_lower else '',
        'upper': string.ascii_uppercase if use_upper else '',
        'digits': string.digits if use_digits else '',
        'special': string.punctuation if use_special else ''
    }
    
    # Ensure at least one character set is selected
    if not any(character_sets.values()):
        print("Error! You must enable at least one character type.")
        return None
    
    all_chars = ''.join(character_sets.values())
    
    # Create password with at least one character from each selected set
    password = []
    for char_type, chars in character_sets.items():
        if chars:
            password.append(random.choice(chars))
    
    # Fill remaining length
    for _ in range(length - len(password)):
        password.append(random.choice(all_chars))
    
    random.shuffle(password)
    return ''.join(password)

def get_user_preferences():
    """Get password requirements from user"""
    print("\n=== PASSWORD GENERATOR ===")
    print("--------------------------")
    
    # Get length
    while True:
        try:
            length = int(input("Password length (8-128): ").strip())
            if 8 <= length <= 128:
                break
            print("Please enter a number between 8 and 128")
        except ValueError:
            print("Invalid input! Please enter a number.")
    
    # Get complexity
    print("\nSelect character types to include:")
    use_lower = input("Include lowercase letters? (y/n): ").lower() == 'y'
    use_upper = input("Include uppercase letters? (y/n): ").lower() == 'y'
    use_digits = input("Include digits? (y/n): ").lower() == 'y'
    use_special = input("Include special characters? (y/n): ").lower() == 'y'
    
    return length, use_lower, use_upper, use_digits, use_special

def main():
    while True:
        length, *complexity = get_user_preferences()
        password = generate_password(length, *complexity)
        
        if password:
            print("\n=== YOUR PASSWORD ===")
            print(password)
            print(f"Length: {len(password)} characters")
            print("----------------------")
        
        if input("\nGenerate another? (y/n): ").lower() != 'y':
            print("\nThank you for using the password generator!")
            break

if __name__ == "__main__":
    main()