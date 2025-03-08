import tkinter as tk
from tkinter import filedialog, messagebox
import itertools

# Function to extract first name from email
def extract_first_name(email):
    first_name = email.split('@')[0].split('.')[0]
    return first_name

# Function to generate all possible number combinations based on max digits
def generate_number_combinations(max_digits):
    number_combinations = []
    for digits in range(1, max_digits + 1):
        for num in itertools.product("0123456789", repeat=digits):
            number_combinations.append(''.join(num))
    return number_combinations

# Function to generate passwords
def generate_passwords(first_name, special_char, number_combinations, fixed_numbers, birth_years):
    passwords = []
    
    # If special_char is empty, don't use it
    special_char = special_char if special_char else ''
    
    # Generate combinations with number patterns
    for num in number_combinations:
        passwords.append(f"{first_name.capitalize()}{special_char}{num}")
        passwords.append(f"{first_name.lower()}{special_char}{num}")
        passwords.append(f"{first_name.upper()}{special_char}{num}")
    
    # Add fixed numbers if provided
    for fixed_number in fixed_numbers:
        fixed_number = fixed_number.strip()
        passwords.append(f"{first_name.capitalize()}{special_char}{fixed_number}")
        passwords.append(f"{first_name.lower()}{special_char}{fixed_number}")
        passwords.append(f"{first_name.upper()}{special_char}{fixed_number}")
    
    # Add birth year ranges if provided
    for year in birth_years:
        passwords.append(f"{first_name.capitalize()}{special_char}{year}")
        passwords.append(f"{first_name.lower()}{special_char}{year}")
        passwords.append(f"{first_name.upper()}{special_char}{year}")
    
    return passwords

# Function to process emails and generate passwords
def process_emails(email_file, special_char, fixed_numbers, max_digits, birth_year_range, output_file):
    try:
        fixed_numbers = fixed_numbers.split(",") if fixed_numbers else []
        max_digits = int(max_digits) if max_digits else 0

        # Generate number combinations if max_digits is provided
        number_combinations = generate_number_combinations(max_digits) if max_digits > 0 else []

        # Generate birth years if birth_year_range is provided
        birth_years = []
        if birth_year_range:
            try:
                start_year, end_year = map(int, birth_year_range.split('-'))
                birth_years = [str(year) for year in range(start_year, end_year + 1)]
            except ValueError:
                raise ValueError("Invalid birth year range. Please use the format 'YYYY-YYYY'.")

        # Process each email
        with open(email_file, 'r') as f:
            emails = f.readlines()

        # Write generated passwords to output file
        with open(output_file, 'w') as f_out:
            for email in emails:
                email = email.strip()
                first_name = extract_first_name(email)
                if first_name:
                    passwords = generate_passwords(first_name, special_char, number_combinations, fixed_numbers, birth_years)
                    for pwd in passwords:
                        f_out.write(f"{pwd}\n")  # Write only the password, no email included

        messagebox.showinfo("Success", f"Passwords generated and saved to {output_file}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to select email file
def select_email_file():
    file_path = filedialog.askopenfilename(title="Select email file", filetypes=[("Text files", "*.txt")])
    email_file_entry.delete(0, tk.END)
    email_file_entry.insert(0, file_path)

# Main GUI window
def create_gui():
    root = tk.Tk()
    root.title("Password Generator Tool")

    # Email file selection
    tk.Label(root, text="Select Email File:").grid(row=0, column=0, padx=10, pady=5)
    global email_file_entry
    email_file_entry = tk.Entry(root, width=40)
    email_file_entry.grid(row=0, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", command=select_email_file).grid(row=0, column=2, padx=10, pady=5)

    # Special character input (optional)
    tk.Label(root, text="Special Character (optional):").grid(row=1, column=0, padx=10, pady=5)
    special_char_entry = tk.Entry(root)
    special_char_entry.grid(row=1, column=1, padx=10, pady=5)

    # Fixed numbers input (optional)
    tk.Label(root, text="Fixed Numbers (optional, comma-separated):").grid(row=2, column=0, padx=10, pady=5)
    fixed_numbers_entry = tk.Entry(root)
    fixed_numbers_entry.grid(row=2, column=1, padx=10, pady=5)

    # Max digits input (optional)
    tk.Label(root, text="Max Digits (optional):").grid(row=3, column=0, padx=10, pady=5)
    max_digits_entry = tk.Entry(root)
    max_digits_entry.grid(row=3, column=1, padx=10, pady=5)

    # Birth year range input (optional)
    tk.Label(root, text="Birth Year Range (optional, e.g., 1980-2000):").grid(row=4, column=0, padx=10, pady=5)
    birth_year_range_entry = tk.Entry(root)
    birth_year_range_entry.grid(row=4, column=1, padx=10, pady=5)

    # Output file name (mandatory)
    tk.Label(root, text="Output File Name:").grid(row=5, column=0, padx=10, pady=5)
    output_file_entry = tk.Entry(root)
    output_file_entry.grid(row=5, column=1, padx=10, pady=5)
    output_file_entry.insert(0, "output.txt")  # Default output file

    # Generate passwords button
    def on_generate_click():
        email_file = email_file_entry.get()
        special_char = special_char_entry.get()
        fixed_numbers = fixed_numbers_entry.get()
        max_digits = max_digits_entry.get()
        birth_year_range = birth_year_range_entry.get()
        output_file = output_file_entry.get()

        # Check if email file and output file name are provided
        if not email_file or not output_file:
            messagebox.showwarning("Input Error", "Please provide the email file and output file name.")
        else:
            process_emails(email_file, special_char, fixed_numbers, max_digits, birth_year_range, output_file)

    tk.Button(root, text="Generate Passwords", command=on_generate_click).grid(row=6, column=1, pady=10)

    root.mainloop()

# Run the GUI
create_gui()

