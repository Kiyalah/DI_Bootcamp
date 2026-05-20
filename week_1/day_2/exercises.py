# 🌟 Exercise 1: Converting Lists into Dictionaries
# Key Python Topics:

# Creating dictionaries
# Zip function or dictionary comprehension


# Instructions

# You are given two lists. Convert them into a dictionary where the first list contains the keys and the second list contains the corresponding values.



# Lists:

# keys = ['Ten', 'Twenty', 'Thirty']
# values = [10, 20, 30]


# Expected Output:

# {'Ten': 10, 'Twenty': 20, 'Thirty': 30}

keys = ['Ten', 'Twenty', 'Thirty']
values = [10, 20, 30]

for key, value in zip(keys, values):
    zipped_dict = dict(zip(keys, values))
    
print (zipped_dict)


# 🌟 Exercise 2: Cinemax #2
# Key Python Topics:

# Looping through dictionaries
# Conditionals
# Calculations


# Instructions

# Write a program that calculates the total cost of movie tickets for a family based on their ages.

# Family members’ ages are stored in a dictionary.
# The ticket pricing rules are as follows:
# Under 3 years old: Free
# 3 to 12 years old: $10
# Over 12 years old: $15


# Family Data:

# family = {"rick": 43, 'beth': 13, 'morty': 5, 'summer': 8}


# Loop through the family dictionary to calculate the total cost.
# Print the ticket price for each family member.
# Print the total cost at the end.


# Bonus:

# Allow the user to input family members’ names and ages, then calculate the total ticket cost.

family = {"rick": 43, 'beth': 13, 'morty': 5, 'summer': 8}

total = 0  

for name, age in family.items():
    if age < 3:
        price = 0
        print("Under 3 years old: Free")
    elif 3 <= age <= 12:
        price = 10
        print("3 to 12 years old: $10")
    else:
        price = 15
        print("Over 12 years old: $15")

    total += price
    print(f"Total price for {name}: ${price}")

print(f"\nTotal price for the family: ${total}")

#Bonus:

family = {}
while True:
    name = input("Enter family member's name (or 'done' to finish): ")
    if name.lower() == 'done':
        break
    age = int(input(f"Enter {name}'s age: "))
    family[name] = age
    
total = 0
for name, age in family.items():
    if age < 3:
        price = 0
        print(f"{name} is under 3 years old: Free")
    elif 3 <= age <= 12:
        price = 10
        print(f"{name} is between 3 and 12 years old: $10")
    else:
        price = 15
        print(f"{name} is over 12 years old: $15")

    total += price
    print(f"Total price for {name}: ${price}")
    
print(f"\nTotal price for the family: ${total}")



# 🌟 Exercise 3: Zara
# Key Python Topics:

# Creating dictionaries
# Accessing and modifying dictionary elements
# Dictionary methods like .pop() and .update()


# Instructions

# Create and manipulate a dictionary that contains information about the Zara brand.



# Brand Information:

# name: Zara
# creation_date: 1975
# creator_name: Amancio Ortega Gaona
# type_of_clothes: men, women, children, home
# international_competitors: Gap, H&M, Benetton
# number_stores: 7000
# major_color: 
#     France: blue, 
#     Spain: red, 
#     US: pink, green


# Create a dictionary called brand with the provided data.
# Modify and access the dictionary as follows:
# Change the value of number_stores to 2.
# Print a sentence describing Zara’s clients using the type_of_clothes key.
# Add a new key country_creation with the value Spain.
# Check if international_competitors exists and, if so, add “Desigual” to the list.
# Delete the creation_date key.
# Print the last item in international_competitors.
# Print the major colors in the US.
# Print the number of keys in the dictionary.
# Print all keys of the dictionary.


# Bonus:

# Create another dictionary called more_on_zara with creation_date and number_stores. Merge this dictionary with the original brand dictionary and print the result.



brand = {
    "name": "Zara",
    "creation_date": 1975,
    "creator_name": "Amancio Ortega Gaona",
    "type_of_clothes": ["men", "women", "children", "home"],
    "international_competitors": ["Gap", "H&M", "Benetton"],
    "number_stores": 7000,
    "major_color": {
        "France": "blue",
        "Spain": "red",
        "US": ["pink", "green"]
    }
}

brand["number_stores"] = 2


print("Zara's clients are:", brand["type_of_clothes"])

brand["country_creation"] = "Spain"

if "international_competitors" in brand:
    brand["international_competitors"].append("Desigual")
    print("Zara's international competitors are:", brand["international_competitors"])

brand.pop("creation_date")

print("Zara's last international competitor is: ", brand["international_competitors"][-1])

print("Zara's major colors in the US are: ", brand["major_color"]["US"])


number_of_keys = len(brand.keys())
print("Number of keys in the brand dictionary:", number_of_keys)

print("All keys in the brand dictionary:", brand.keys())

#Bonus
more_on_zara = {
    "creation_date": 1975,
    "number_stores": 10000
}

brand.update(more_on_zara)
print("Updated brand dictionary:", brand)



# 🌟 Exercise 4 : Some Geography
# Goal: Create a function that describes a city and its country.

# Key Python Topics:

# Functions with multiple parameters
# Default parameter values
# String formatting


# Step 1: Define a Function with Parameters

# Define a function named describe_city().
# This function should accept two parameters: city and country.
# Give the country parameter a default value, such as “Unknown”.


# Step 2: Print a Message

# Inside the function, set up the code to display a sentence like “ is in “.
# Replace <city> and <country> with the parameter values.


# Step 3: Call the Function

# Call the describe_city() function with different city and country combinations.
# Try calling it with and without providing the country argument to see the default value in action.
# Example: describe_city("Reykjavik", "Iceland") and describe_city("Paris").


# Expected Output:

# Reykjavik is in Iceland.
# Paris is in Unknown.

def describe_city(city, country="Unknown"):
    print(f"{city} is in {country}.")


describe_city("Reykjavik", "Iceland")
describe_city("Paris")



# 🌟 Exercise 5 : Random
# Goal: Create a function that generates random numbers and compares them.

# Key Python Topics:

# random module
# random.randint() function
# Conditional statements (if, else)


# Step 1: Import the random Module

# At the beginning of your script, use import random to access the random number generation functions.


# Step 2: Define a Function with a Parameter

# Create a function that accepts a number between 1 and 100 as a parameter.


# Step 3: Generate a Random Number

# Inside the function, use random.randint(1, 100) to generate a random integer between 1 and 100.


# Step 4: Compare the Numbers

# If they are the same, print a success message. Otherwise, print a fail message and display both numbers.


# Step 5: Call the Function

# Call the function with a number between 1 and 100.


# Expected Output:

# Success! (if the numbers match)
# Fail! Your number: 50, Random number: 23 (if they don't match)


import random

def generate_random_number(number_1):
    number_2 = random.randint(1, 100)

    if number_1 == number_2:
        print("Success!")
    else:
        print(f"Failed! Your number: {number_1}, Random number: {number_2}")

generate_random_number(50)



# 🌟 Exercise 6 : Let’s create some personalized shirts !
# Goal: Create a function to describe a shirt’s size and message, with default values.

# Key Python Topics:

# Functions with parameters and default values
# Keyword arguments


# Step 1: Define a Function with Parameters

# Define a function called make_shirt().
# This function should accept two parameters: size and text.


# Step 2: Print a Summary Message

# Set up the function to display a sentence summarizing the shirt’s size and message.


# Step 3: Call the Function



# Step 4: Modify the Function with Default Values

# Modify the make_shirt() function so that size has a default value of “large” and text has a default value of “I love Python”.


# Step 5: Call the Function with Default and Custom Values

# Call make_shirt() to make a large shirt with the default message.
# Call make_shirt() to make a medium shirt with the default message.
# Call make_shirt() to make a shirt of any size with a different message.


# Step 6 (Bonus): Keyword Arguments

# Call make_shirt() using keyword arguments (e.g., make_shirt(size="small", text="Hello!")).


# Expected Output:

# The size of the shirt is large and the text is I love Python.
# The size of the shirt is medium and the text is I love Python.
# The size of the shirt is small and the text is Custom message.

def make_shirt(size, text):
    print(f"The shirt size is {size} and the message is '{text}'.")
    
make_shirt("M", "I love Basketball")

#Step 4
def make_shirt(size="large", text="I love Python"):
    print(f"The shirt size is {size} and the message is '{text}'.")

make_shirt()
make_shirt(size="medium")
make_shirt(text="I love JavaScript")

make_shirt(size="small", text="Hello!")





def get_random_temp():
    return random.randint(-10, 40)


def main():
    temp = get_random_temp()
    print (f"The current temperature is {temp}°C.")
    if temp < 0:
        print("Brrr, that’s freezing! Wear some extra layers today.")
    elif 0 <= temp < 16:
        print("Quite chilly! Don’t forget your coat.")
    elif 16 <= temp < 23:
        print("Nice weather.")
    elif 24 <= temp < 32:
        print("A bit warm, stay hydrated.")
    elif 32 <= temp < 40:
        print("It’s really hot! Stay cool.")
        

