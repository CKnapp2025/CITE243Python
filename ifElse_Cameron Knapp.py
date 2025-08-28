# Mood to Movie Interpreter by Cameron Knapp

mood = input("What kind of mood are you in? (happy, sad, excited, thoughtful): ")
time = input("Do you want a short movie (under 2 hours) or a long movie (2+ hours)? (short/long): ")

if mood == "happy":
    if time == "short":
        print("Watch 'Ferris Bueller's Day Off' (fun and under 2 hours).")
    else:
        print("Watch 'Superbad' (a longer comedy night with friends).")

elif mood == "sad":
    if time == "short":
        print("Try 'Good Will Hunting' (a heartfelt but shorter watch).")
    else:
        print("Watch 'The Pursuit of Happyness' for an emotional journey.")

elif mood == "excited":
    if time == "short":
        print("Go for 'Mad Max: Fury Road' — pure adrenaline in under 2 hours!")
    else:
        print("Watch 'Avengers: Endgame' or 'Inception' for a longer thrill ride.")

elif mood == "thoughtful":
    if time == "short":
        print("Watch 'The Truman Show' — thoughtful and under 2 hours.")
    else:
        print("Go for 'Interstellar' or 'The Social Network' for a deep dive.")

else:
    print("Not sure? Pick 'Back to the Future' — a classic for any mood or time!")
