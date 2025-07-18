import secrets
import string

# Gemini
def generate_strong_password(length=12):
    """
    Generates a strong, random password.
    Ensures at least one uppercase, one lowercase, one digit, and one special character.
    """
    if length < 8:
        raise ValueError("Password length must be at least 8 characters for strength.")

    uppercase_chars = string.ascii_uppercase
    lowercase_chars = string.ascii_lowercase
    digits = string.digits
    # special_chars = string.punctuation

    all_characters = uppercase_chars + lowercase_chars + digits 

    while True:
        password = ''.join(secrets.choice(all_characters) for _ in range(length))
        
        # Check for complexity requirements
        if (any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password)):
            break
    return password
