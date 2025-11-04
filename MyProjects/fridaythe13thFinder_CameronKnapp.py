"""
===========================================================
Program Name: Friday the 13th in Time
Author: Cameron Knapp
Date: 2025-11-04
Description:
    Interactive timeline tool for finding Friday the 13th dates.
    Step 1: User chooses 'forward' or 'backward'.
    Step 2: User provides a target year with strict validation.
       - forward: year must be >= current year and <= 2125
       - backward: year must be <= current year and >= 1925
    After completion, the user can type 'done' to end or
    anything else to restart the program.
Usage:
    Run the script and follow on-screen prompts.
    (Programmer's Note: It's really that simple!)
===========================================================
"""

import datetime

# Date format function for cleanliness...
def format_date(d: datetime.date) -> str:
    return d.strftime("%B %d, %Y")


# Print the introduction page (this is going to get called back a lot)...
def print_intro():
    """Display the introduction and basic instructions."""
    print("==========================")
    print("Friday the 13th, A Timeline Perspective")
    print("==========================")
    print("Type 'forward' followed by the year of how far forward you'd like to look into the future.")
    print("Type 'backward' followed by the year of how far backward you'd like to look into the past.")
    print("==========================")


# Core loop for handling user choices and outputting timelines...
def run_program():
    today = datetime.date.today()
    one_day = datetime.timedelta(days=1)

    while True:
        # Choose forward or backward...
        print_intro()
        func = input("> ").strip().lower()

        # Handle for nonsensical inputs...
        if func not in ("forward", "backward"):
            print("That is not a valid function, try again.\n")
            continue  # Restart at the main menu

        # 'Forward' function logic...
        if func == "forward":
            while True:
                print("\nI see, until what year would you like to prepare...? (I can only look until 2125...)")
                year_str = input("> ").strip()

                # Handle for nonsensical inputs...
                if not year_str.isdigit():
                    print("That is an invalid year, try again.\n")
                    break  # If not return question...

                target = int(year_str)

                # Is before 2126?
                if target > 2125:
                    print("I cannot see that far into the future, try again.\n")
                    continue  # If not return question...
                elif target < today.year:
                    print("If you would like to look into the past, try the 'backward' function.\n")
                    break  # Is attempt before 2025? Then...

                # If correct...
                print(f"\nFriday the 13ths between {today.year} and {target}:\n")
                cur = today
                while cur.year <= target:
                    if cur.day == 13 and cur.weekday() == 4:
                        print(f"--> {format_date(cur)}")
                    cur += one_day

                print("\nTimeline drawn, now you are ready...")
                return  # End function, move to post-run prompt...

            # Invalid or redirected year sends user back to main menu...
            continue

        # 'Backward' function logic...
        else:
            while True:
                print("\nI see, from what year would you like to begin looking into the past? (I can only look back as far as 1925.)")
                year_str = input("> ").strip()

                # Handle for nonsensical inputs...
                if not year_str.isdigit():
                    print("That is an invalid year, try again.\n")
                    break  # If not return question...

                target = int(year_str)

                # Is after 1924?
                if target < 1925:
                    print("I cannot see that far back into the past, try again.\n")
                    continue
                elif target > today.year:
                    print("If you would like to look into the future, try the 'forward' function.\n")
                    break  # Is attempt after 2025? Then...

                # If correct...
                print(f"\nFriday the 13ths from {today.year} back to {target}:\n")
                cur = today
                while cur.year >= target:
                    if cur.day == 13 and cur.weekday() == 4:
                        print(f"--> {format_date(cur)}")
                    cur -= one_day

                print("\nTimeline drawn, now you are ready...")
                return  # End function, move to post-run prompt...

            # Invalid or redirected year sends user back to main menu...
            continue


# Post-run "loop" function...
def post_run_prompt():
    while True:
        print("\nType 'done' to end the program immediately.")
        print("Type anything else to restart the program.\n")
        choice = input("> ").strip().lower()

        if choice == "done":
            print("Farewell...")
            break          # Exit Program...
        else:
            print("\nPreparing...\n")
            run_program()  # Restart from beginning...


# Run main flow first, then run post flow after main flow is completed!
if __name__ == "__main__":
    run_program()
    post_run_prompt()
