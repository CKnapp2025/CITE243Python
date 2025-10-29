"""
===========================================================
Program Name: Meal Database 
Author: Cameron Knapp
Date: 2025-10-29
Description:
    This program uses an SQLite database to store meals
    and their associated ingredients. Users can add new
    meals with ingredients, query a meal to see its
    ingredients, or query an ingredient to see which
    meals use it. The database is automatically created
    if it does not exist. Includes a safeguard to prevent
    users from making an existing ingredient its own meal.

Usage:
    1. Run the script using Python 3.x.
    2. When prompted:
         • To add a meal: enter it in the format
           meal:ingredient1,ingredient2,...
         • To query a meal or ingredient: type its name.
         • To exit: type 'quit'
    3. The program will store all data in meals.db in
       the same folder as this script.
===========================================================
"""

import sqlite3

# Connects to or creates a new database file if missing...
conn = sqlite3.connect('meals.db')
cursor = conn.cursor()

# Create tables if they don't already exist...
cursor.execute("""
CREATE TABLE IF NOT EXISTS meals (
    name TEXT UNIQUE
) STRICT
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ingredients (
    name TEXT,
    meal_id INTEGER,
    FOREIGN KEY(meal_id) REFERENCES meals(rowid)
) STRICT
""")

conn.commit()

# Display the user welcome and instructions splash text...
print("Welcome to the Meal Ingredients Database!")
print("- To make a new meal write > 'meal_name: ingredient, ingredient, ingredient,...'")
print("- To list a meal's ingredients write > 'meal_name'")
print("- To list what meals use any ONE ingredient write > 'ingredient'")
print("Enter 'quit' to exit at any time.\n")

# The Loop...
while True:
    user_input = input("> ").strip()

    # Exit conditioning... /// hopefully you don't have a meal or ingredient named quit!
    if user_input.lower() == 'quit':
        print("Your meal database has been saved. Goodbye!")
        break

    # Handle for adding new meals...
    if ':' in user_input:
        try:
            meal_name, ingredients_str = user_input.split(':', 1)
            meal_name = meal_name.strip()
            ingredients = [ing.strip() for ing in ingredients_str.split(',') if ing.strip()]

            # Handle for improper meal format...
            if not meal_name or not ingredients:
                print("Invalid format. Example: onigiri:rice,nori,salt")
                continue

            # Handle if a new meal already exists as an ingredient so nothing clashes weirdly...
            cursor.execute("SELECT DISTINCT name FROM ingredients WHERE name = ?", (meal_name,))
            ingredient_conflict = cursor.fetchone()
            if ingredient_conflict:
                print("You can't make an existing ingredient its own meal!")
                continue

            # Insert a properly inputted new meal...
            cursor.execute("INSERT OR IGNORE INTO meals (name) VALUES (?)", (meal_name,))
            conn.commit()

            cursor.execute("SELECT rowid FROM meals WHERE name = ?", (meal_name,))
            meal_id = cursor.fetchone()[0]

            # Insert the ingredients to that meal...
            for ing in ingredients:
                cursor.execute("INSERT INTO ingredients (name, meal_id) VALUES (?, ?)", (ing, meal_id))
            conn.commit()

            print(f"Meal added: {meal_name}")

        except Exception as e:
            print(f"Error adding meal: {e}")

    else:
        # Handle listing ingredients or meals using an ingredient...
        name = user_input

        # Is a meal?
        cursor.execute("SELECT rowid FROM meals WHERE name = ?", (name,))
        meal_row = cursor.fetchone()

        if meal_row:
            meal_id = meal_row[0]
            cursor.execute("SELECT name FROM ingredients WHERE meal_id = ?", (meal_id,))
            ingredients = cursor.fetchall()

            print(f"Ingredients of {name}:")
            for ing in ingredients:
                print(f"  {ing[0]}")
            continue

        # Is an ingredient?
        cursor.execute("SELECT DISTINCT meals.name FROM meals "
                       "JOIN ingredients ON meals.rowid = ingredients.meal_id "
                       "WHERE ingredients.name = ?", (name,))
        meals_using_ing = cursor.fetchall()

        # Handle for any strange or invalid inputs...
        if meals_using_ing:
            print(f"Meals that use {name}:")
            for meal in meals_using_ing:
                print(f"  {meal[0]}")
        else:
            print("No matches found.")

# And...done!
conn.close()
