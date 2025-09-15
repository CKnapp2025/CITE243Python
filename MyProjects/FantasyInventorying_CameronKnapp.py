# Fantasy Inventorying by Cameron Knapp [243]

def display_inventory(inventory):                               # Definining what 'the inventory' is.
    print("Inventory:")
    item_total = 0
    for k, v in inventory.items():
        print(str(v) + " " + k)
        item_total += v
    print("Total Items: " + str(item_total))

def add_to_inventory(inventory, added_items):                   # Add Additional Loot to Inventory...
    for item in added_items:
        if item in inventory:
            inventory[item] += 1
        else:
            inventory[item] = 1
    return inventory

stuff = {'rope': 1, 'torch': 6, 'gold coin': 42,                # Example Inventory/Dragon Loot, Maybe adding an input here would make sense as a standalone, but as a game, just like this makes sense.
         'dagger': 1, 'arrow': 12}
dragon_loot = ['gold coin', 'dagger', 'gold coin',
               'gold coin', 'ruby']

display_inventory(stuff)                                        # Print initial inventory on terminal.
print("\nYou have slain the dragon! Please take the loot...\n")

stuff = add_to_inventory(stuff, dragon_loot)                    # Adding the loot to the inventory.

display_inventory(stuff)                                        # Print the updated inventory.
