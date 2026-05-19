# 📝 Exercise 1: What is the Season?


# 1. Ask the user to input a month (1 to 12).
# 2. Display the season of the month received:
# - Spring runs from March (3) to May (5)
# - Summer runs from June (6) to August (8)
# - Autumn runs from September (9) to November (11)
# - Winter runs from December (12) to February (2)

month = int(input("Enter the month 1-12: "))

if month >= 3 and month <= 5:
    print("Spring")
elif month >= 6 and month <= 8:
    print("Summer")
elif month >= 9 and month <= 11:
    print("Autumn")
elif month == 12 or month == 1 or month == 2:
    print("Winter")
    
    
    
 
#  📝 Exercise 2: For Loop


# Key Python Topics:

# Loops (for)
# Range and indexing


# Instructions:

# Write a for loop to print all numbers from 1 to 20, inclusive.
# Write another for loop that prints every number from 1 to 20 where the index is even.
   
number = range(1, 13)
for i in number:
    print (i)
    
for i in number:
    if i % 2 == 0:
        print(i)



# 📝 Exercise 4: Check the index


# Using this variable:

# names = ['Samus', 'Cortana', 'V', 'Link', 'Mario', 'Cortana', 'Samus']

# Ask a user for their name, if their name is in the names list print out the index of the first occurrence of the name.

# Example: if input is Cortana we should be printing the index 1

names = ['Samus', 'Cortana', 'V', 'Link', 'Mario', 'Cortana', 'Samus']

user_name = str(input("Enter a name: "))
if user_name in names:
    print(names.index(user_name))
else: 
    print("Name not found in the list.")
    
    


# 📝 Exercise 5: Greatest Number


# Ask the user for 3 numbers and print the greatest number.

# Test Data:

# Input the 1st number: 25
# Input the 2nd number: 78
# Input the 3rd number: 87

# The greatest number is: 87

n1 = int(input("Enter the first number: "))
n2 = int(input("Enter the second number: "))
n3 = int(input("Enter the third number: "))

numbers = [n1, n2, n3]
highest = 0

for i in numbers:
    if i > highest:
        highest = i
    
print("The highest number is:", highest)


# 📝 Exercise 6: Random number


# Ask the user to input a number from 1 to 9 (including).
# Get a random number between 1 and 9. Hint: random module.
# If the user guesses the correct number print a message that says “Winner”.
# If the user guesses the wrong number print a message that says “Better luck next time.”
# Bonus: use a loop that allows the user to keep guessing until they want to quit.
# Bonus 2: on exiting the loop, tally up and display total games won and lost.


from random import random
number = int(input("Enter a number from 1 to 9(including): "))
random_number = random.randint(1, 9)

if number == random_number:
    print("Congratulations! You guessed the number.")
else:
    print("Sorry, the number was", random_number)
    print("Better luck next time!")
    
    
#Bonus
from random import randint

random_number = randint(1, 9)

while True:
    try:
        number = int(input("Enter a number from 1 to 9 (inclusive): "))
    except ValueError:
        print("Please enter a valid integer.")
        continue

    if number == random_number:
        print("Congratulations! You guessed the number.")
        break

    print("Try again")
    


#Bonus 2
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
