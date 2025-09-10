# Debugging the Coin Toss by Cameron Knapp [243]

import random

guess = ''
while guess not in ('heads', 'tails'):
    print('Guess the coin toss! Enter heads or tails:')
    guess = input()

toss = random.randint(0, 1)  # 0 is tails, 1 is heads <-- Wasn't actually being done in the original program. It would generate an integer then immediately compare that to the input.
if toss == 0:
    toss = 'tails'           # Changed to convert '0' to the string 'tails' instead of being just an integer.
else:
    toss = 'heads'           # Changed to convert '1' to the string 'heads' instead of being just an integer.

if toss == guess:            # Program will now compare two strings instead of an integer & string which would originally always be 'False'.
    print('You got it!')
else:
    print('Nope! Guess again!')
    guess = input()
    if toss == guess:        # Same change as line 16.
        print('You got it!')
    else:
        print('Nope. You are really bad at this game.')
