"""
===========================================================
Program Name: Selectively Copying Files
Author: Cameron Knapp
Date: 2025-09-29
Description:
    This program walks through a folder tree and searches
    for files with a specific file extension (such as .pdf
    or .jpg). All matching files are copied into a new
    destination folder. The program validates the source
    folder, automatically creates the destination folder
    if it does not exist, and shows how many files were
    copied.

Usage:
    1. Run the script using Python 3.x.
    2. Enter the folder path you want to search in. The
       program will not continue until a valid path is
       provided.
    3. Enter the destination folder where matching files
       will be copied. If this folder does not exist, it
       will be created automatically.
    4. Enter the file extension you want to search for
       (example: .pdf, .jpg, .png). The program will copy
       every file with that extension, so be cautious.
===========================================================
"""

import os                                                               # For walking through folder tree...
import shutil                                                           # For copying files...

while True:
    print("Enter the folder path to search in...")                      # Grab source folder from user...
    source_folder = input("> ")
    if os.path.isdir(source_folder):                                    # Check if the directory is valid...
        break
    else:
        print("Enter a VALID folder path to search in:")                # If not...

print("Enter the folder path where files will be copied...")            # Grab destination folder from user...
print("PLEASE NOTE: If the directory you specify here does not exist, this program will make one for you, so be cautious.")
destination_folder = input("> ")
os.makedirs(destination_folder, exist_ok=True)                          # Create directory if not exist...

print("Enter the file extension to search for (e.g. .pdf or .png)...")  # Grab the file extension from user...
print("PLEASE NOTE: This program will copy EVERY file with the extension you specify, so be careful...")
file_extension = input("> ")

count = 0                                                               # For fun and for summary...
for foldername, subfolders, filenames in os.walk(source_folder):        # Walk through file tree...
    for filename in filenames:
        if filename.lower().endswith(file_extension.lower()):
            file_path = os.path.join(foldername, filename)
            print(f"Copying: {file_path}")                              # Copy & list each file for logging...
            shutil.copy(file_path, destination_folder)
            count += 1

print(f"\nAll matching files have been copied successfully! ({count} files copied.)") # Print the summary!
