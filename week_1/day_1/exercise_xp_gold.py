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

        
