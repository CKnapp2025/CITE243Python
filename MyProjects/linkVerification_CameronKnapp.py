"""
===========================================================
Program Name: Link Verification
Author: Cameron Knapp
Date: 2025-10-13
Description:
    This program takes the URL of a web page, scans all
    hyperlinks (<a> tags), and checks whether each linked
    page is valid or broken. A link is considered broken if
    it returns a 404 (Not Found) status code or cannot be
    reached. The program prints out all broken links found
    on the page.

Usage:
    1. Run this in your command prompt: 'pip install requests beautifulsoup4'
    before running the script.
    2. Run the script using Python 3.x. 'python linkVerification_CameronKnapp.py'
    3. When prompted, enter a full website URL such as 'https://example.com'.
    4. The program will check all links on that page and display any broken ones.
    5. If you want to save a file of the output just run:
    'python link_Verification_CameronKnapp.py > results.txt'
===========================================================
"""

import requests
from bs4 import BeautifulSoup

url = input("Enter the full URL of the web page to check: ")                # Get URL input...

try:                                                                        # Attempt to download the entire webpage...
    response = requests.get(url)
    response.raise_for_status()                                             # Raises an error for any bad inputs and quits...
except requests.exceptions.RequestException as e:
    print(f"Error accessing the URL: {e}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")                                 # Parse the page's content...

links = soup.find_all("a")                                                         # Find all <a> links...
print(f"\nFound {len(links)} links on the page. Checking for broken links...\n")   # Give the user a total number of links and the advise...

broken_links = []                                                                  # Checking each link...

for link in links:
    href = link.get("href")

    if not href or href.startswith("#"):                                     # Skip if link has no href or is just an anchor...
        continue

    if href.startswith("/"):                                                 # Handle any relative urls...
        href = requests.compat.urljoin(url, href)

    try:
        res = requests.head(href, allow_redirects=True, timeout=5)
        if res.status_code == 404:
            print(f"Broken link found: {href}")                              # Display any broken link...
            broken_links.append(href)
        else:
            print(f"Working link: {href}")                                   # Display a the status that a link is being worked (haha)...
    except requests.exceptions.RequestException:
        print(f"Could not reach: {href}")                                    # Display any link that returns a RequestException error...
        broken_links.append(href)

print("\n===== SUMMARY =====")                                               # Display a clean summary...
if broken_links:
    print(f"Broken links found ({len(broken_links)}):")                      # Display total broken links...
    for bl in broken_links:
        print(f" - {bl}")                                                    # Print the links...
else:
    print("No broken links found! All links are valid.")                     # If by some miracle every link works, a success message will show! :)
