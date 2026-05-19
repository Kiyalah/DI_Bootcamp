from random import randint

random_number = randint(1, 9)
tries = 0

while True:
    try:
        number = int(input("Enter a number from 1 to 9 (inclusive): "))
    except ValueError:
        print("Please enter a valid integer.")
        continue

    tries += 1

    if number == random_number:
        print(f"Congratulations! You guessed the number in {tries} tries.")
        break

    print("Try again")