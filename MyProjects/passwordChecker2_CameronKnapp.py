"""
===========================================================
Program Name: Password Strength Checker v2
Author: Cameron Knapp
Date: 2025-09-23
Description:
    This program checks whether a password is strong by
    using regular expressions to validate specific rules.
    A strong password must be at least eight characters long,
    contain both uppercase and lowercase characters,
    and have at least one digit.

Usage:
    Run the script using Python 3.x. The program asks the
    user to input a password idea and evaluates its strength.
    If the password is weak OR INVALID, the user must try again.
===========================================================
"""

import re      # Import regex module...
import time    # Import time for sleep function...

def strong_password(password):                                # Define function to check password strength...
    if len(password) < 8:                                     # Rule 1: At least 8 characters...
        return False
    if not re.search(r'[A-Z]', password):                     # Rule 2: At least one uppercase letter...
        return False
    if not re.search(r'[a-z]', password):                     # Rule 3: At least one lowercase letter...
        return False
    if not re.search(r'[0-9]', password):                     # Rule 4: At least one digit...
        return False
    return True                                               # Passed all checks...

print("Welcome to the Strong Password Checker!")
print("Don't worry — I won't remember your password!")
print("Your secret is safe with me!\n")

while True:                                                   # Keep looping until success...
    user_password = input("Please enter your desired password idea: ")

    # --- New Checks ---
    if user_password == "":                                   # Feedback: Empty password...
        print("Your password actually has to exist...try again!\n")
        continue                                              # Restart loop and re-prompt...

    if len(user_password) >= 20:                              # Feedback: Too long password...
        print("Are you really going to remember that? Try again!\n")
        continue                                              # Restart loop and re-prompt...

    print("Analyzing your password...\n")
    time.sleep(3)                                             # Wait 3 seconds just for fun... :)

    if strong_password(user_password):
        print("That’s a strong password! Well done.")
        break                                                 # Exit once strong password given...
    else:
        print("That password is NOT strong enough.")
        print("Remember: A good password should be at least 8 characters, one uppercase, one lowercase, and one digit.")
        print("Try again!\n")                                # Loop continues and re-prompts automatically!
