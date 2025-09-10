def comma_code(items):
    return ', '.join(items)                     # Joins items input together.


while True:                                     # Loop until the list is a valid or complete list.
    items = []                                  # An Empty List to start.
    print("Hello! What would you like to add to the list?")

    while True:                                 # Keep asking for items
        item = input("> ")
        if item == "":                          # Stop if user presses Enter.
            break
        items.append(item)                      # Adds an additional item to the list & outputs for additional inputs.
        print("Anything else? (Press 'Enter' if done.)")

    if len(items) == 0:                         # Handle for nothing being put onto the list.
        print("Hey, you can't have an empty list. Try again!")
        continue

    print("Okay, here is your list:")           # As long as the list isn't empty AND the user has input a blank ('Enter') the program stops.
    print(comma_code(items))                    # Prints completed list.
    break
