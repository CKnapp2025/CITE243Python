# For & While Loops As One -- Cameron Knapp [243] 

while True:
    choice = input("Would you like me to count to ten using the 'For' or 'While' method? ")

    if choice == "for":
        print("Counting to 10 using FOR...")
        for i in range(1, 11):
            print(i)
        print("FOR loops are neat right? Let us do it again!")

    elif choice == "while":
        print("Counting to 10 using WHILE...")
        i = 1
        while i <= 10:
            print(i)
            i += 1
        print("WHILE loops are neat right? Let us do it again!")

    else:
        continue
