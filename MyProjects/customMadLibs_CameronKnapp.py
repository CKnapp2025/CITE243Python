"""
===========================================================
Program Name: Custom Mad Libs Generator v4
Author: Cameron Knapp
Date: 2025-09-23
Description:
    This program reads a specific text file containing placeholders
    (ADJECTIVE, NOUN, ADVERB, VERB) and prompts the user to
    replace each occurrence in the order as it appears. The
    completed story is then printed and saved to a new file.

Usage:
    1. Create or Modify the text file named 'madlibs_template.txt' that
     was paired with this program.
    2. Make sure you use valid placeholders such as ADJECTIVE, NOUN,
    ADVERB, and VERB.
    3. Run the script using Python 3.x.
    4. The program will prompt you for each placeholder in
    sequence.
    5. The final result will be printed and saved to madlibs_result.txt.
===========================================================
"""

import re                                                              # Regex...

with open("madlibs_template.txt", "r") as file:                        # Read the template file...
    text = file.read()

pattern = re.compile(r'ADJECTIVE|NOUN|ADVERB|VERB')                    # REGEX to match placeholders...

while True:
    match = pattern.search(text)                                       # Replace the placeholders in order starting from the first instance...
    if match is None:                                                  # If no more placeholders, stop...
        break
    word = match.group()                                               # Extract which placeholder it is...
    article = "an" if word[0] in "AEIOU" else "a"                      # Grammar: use 'an' if starts with vowel (the following was suggested by ChatGPT to save on multiple print cycles)...
    user_input = input(f"Enter {article} {word.lower()}: ")
    text = text[:match.start()] + user_input + text[match.end():]      # Replace just that one...

print("\nHere is/are your Mad Lib(s):\n")                              # Print the resulting story...
print(text)

with open("madlibs_result.txt", "w") as file:                          # Save to a new or the existing file!
    file.write(text)
print("\nCONSOLE: Your mad libs have been saved to 'madlibs_result.txt'!")
