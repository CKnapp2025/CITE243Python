"""
===========================================================
Program Name: Bean Counter Corrector
Author: Cameron Knapp
Date: 2025-10-22
Description:
    This program connects to a public Google Sheets
    spreadsheet containing data on beans per jar,
    number of jars, and total beans. It automatically
    checks every row to verify that the TOTAL BEANS
    column correctly equals BEANS PER JAR * JARS.
    If it finds any inconsistencies, it lists all the rows
    that contain incorrect totals.

Usage:
    1. Run the script using Python 3.x.
    2. Make sure the 'ezsheets' module is installed.
       (Install with: pip install ezsheets)
    3. The first time you use ezsheets, a browser will
       open to log into your Google account. Grant
       permission, and credentials will be saved.
    4. Run this script. It will connect to the shared
       Bean Counter spreadsheet at:
       'https://docs.google.com/spreadsheets/d/1jDZEdvSIh4TmZxccyy0ZXrH-ELlrwq8_YYiZrEOB4jg'
===========================================================
"""

import ezsheets  # Used to access Google Sheets data through the API

ss = ezsheets.Spreadsheet('1jDZEdvSIh4TmZxccyy0ZXrH-ELlrwq8_YYiZrEOB4jg')        # Connect to the specified sheet via the ID...

sheet = ss.sheets[0]                                                             # Direct to the first page of the spreadsheet...

print("Checking spreadsheet for incorrect totals...\n")                          # I don't know why I'm making this note. :)

errors_found = 0                                                                 # There's only one error, but in case there were multiple...

for rowNum in range(2, sheet.rowCount + 1):                                      # Check each row skipping over the first row since it's a header...
    row = sheet.getRow(rowNum)

    if row[0] == '' or row[1] == '' or row[2] == '':                             # Handle for empty rows...
        continue

    try:
        beans_per_jar = int(row[0])                                              # Convert string values to integers...
        jars = int(row[1])
        total_beans = int(row[2])

        if beans_per_jar * jars != total_beans:                                  # Compare calculated total with sheet total...
            print(f"[!] Error found in row {rowNum}: "                           # If inconsistency is found...
                  f"{beans_per_jar} × {jars} = {beans_per_jar * jars}, "
                  f"but sheet says {total_beans}.")
            errors_found += 1

    except ValueError:
        continue                                                                 # Handle for rows containing anything but numbers...

if errors_found == 0:                                                            # Print results!
    print("All totals appear to be correct!")
else:
    print(f"\nCheck complete. {errors_found} incorrect row(s) found.")

print("\nProcess finished.")
