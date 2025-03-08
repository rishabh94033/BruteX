import itertools
import os

# Function to extract first name from email
def extract_first_name(email):
    return email.split('@')[0].split('.')[0]

# Function to generate all possible number combinations based on max digits
def generate_number_combinations(max_digits):
    number_combinations = []
    for digits in range(1, max_digits + 1):
        for num in itertools.product("0123456789", repeat=digits):
            number_combinations.append(''.join(num))
    return number_combinations

# Function to generate passwords
def generate_passwords(first_name, special_char, number_combinations, fixed_numbers):
    passwords = []
    for num in number_combinations:
        passwords.append(f"{first_name.capitalize()}{special_char}{num}")
        passwords.append(f"{first_name.lower()}{special_char}{num}")
        passwords.append(f"{first_name.upper()}{special_char}{num}")
    
    for fixed_number in fixed_numbers:
        fixed_number = fixed_number.strip()
        passwords.append(f"{first_name.capitalize()}{special_char}{fixed_number}")
        passwords.append(f"{first_name.lower()}{special_char}{fixed_number}")
        passwords.append(f"{first_name.upper()}{special_char}{fixed_number}")
    
    return passwords

# Main function to process emails and generate passwords
def process_emails(email_file, output_file):
    # Check if the email file exists
    if not os.path.exists(email_file):
        print(f"Error: The file '{email_file}' does not exist. Please create it and try again.")
        return

    # Ask user for inputs
    try:
        special_char = input("Enter a special character to use (e.g., @, #, !): ").strip()
        fixed_numbers_input = input("Enter fixed numbers to append, separated by commas (e.g., 2004, 2005, 2006): ").strip()
        fixed_numbers = fixed_numbers_input.split(",")
        max_digits = int(input("Enter the maximum number of digits (e.g., 1, 2, 3): ").strip())
    except ValueError:
        print("Invalid input. Please enter correct values.")
        return

    # Generate all possible number combinations
    number_combinations = generate_number_combinations(max_digits)

    # Open the file containing emails and read line by line
    try:
        with open(email_file, 'r') as f:
            emails = [email.strip() for email in f.readlines()]
    except Exception as e:
        print(f"Error reading file '{email_file}': {e}")
        return

    # Open the output file to save the results
    try:
        with open(output_file, 'w') as f_out:
            for email in emails:
                first_name = extract_first_name(email)
                passwords = generate_passwords(first_name, special_char, number_combinations, fixed_numbers)
                for pwd in passwords:
                    f_out.write(f"{email}:{pwd}\n")
        print(f"Passwords generated and saved to '{output_file}'")
    except Exception as e:
        print(f"Error writing to file '{output_file}': {e}")

# Example usage
email_file = "email.txt"  # Input file with emails
output_file = "output.txt"  # Output file to save generated passwords

if __name__ == "__main__":
    process_emails(email_file, output_file)

