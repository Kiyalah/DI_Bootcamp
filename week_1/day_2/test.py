# family = {"rick": 43, 'beth': 13, 'morty': 5, 'summer': 8}

# total = 0  

# for name, age in family.items():
#     if age < 3:
#         price = 0
#         print("Under 3 years old: Free")
#     elif 3 <= age <= 12:
#         price = 10
#         print("3 to 12 years old: $10")
#     else:
#         price = 15
#         print("Over 12 years old: $15")

#     total += price
#     print(f"Total price for {name}: ${price}")

# print(f"\nTotal price for the family: ${total}")


# family = {}
# while True:
#     name = input("Enter family member's name (or 'done' to finish): ")
#     if name.lower() == 'done':
#         break
#     age = int(input(f"Enter {name}'s age: "))
#     family[name] = age
    
# total = 0
# for name, age in family.items():
#     if age < 3:
#         price = 0
#         print(f"{name} is under 3 years old: Free")
#     elif 3 <= age <= 12:
#         price = 10
#         print(f"{name} is between 3 and 12 years old: $10")
#     else:
#         price = 15
#         print(f"{name} is over 12 years old: $15")

#     total += price
#     print(f"Total price for {name}: ${price}")
    
# print(f"\nTotal price for the family: ${total}")



# brand = {
#     "name": "Zara",
#     "creation_date": 1975,
#     "creator_name": "Amancio Ortega Gaona",
#     "type_of_clothes": ["men", "women", "children", "home"],
#     "international_competitors": ["Gap", "H&M", "Benetton"],
#     "number_stores": 7000,
#     "major_color": {
#         "France": "blue",
#         "Spain": "red",
#         "US": ["pink", "green"]
#     }
# }

# brand["number_stores"] = 2


# print("Zara's clients are:", brand["type_of_clothes"])

# brand["country_creation"] = "Spain"

# if "international_competitors" in brand:
#     brand["international_competitors"].append("Desigual")
#     print("Zara's international competitors are:", brand["international_competitors"])

# brand.pop("creation_date")

# print("Zara's last international competitor is: ", brand["international_competitors"][-1])

# print("Zara's major colors in the US are: ", brand["major_color"]["US"])


# number_of_keys = len(brand.keys())
# print("Number of keys in the brand dictionary:", number_of_keys)

# print("All keys in the brand dictionary:", brand.keys())

# #Bonus
# more_on_zara = {
#     "creation_date": 1975,
#     "number_stores": 10000
# }

# brand.update(more_on_zara)
# print("Updated brand dictionary:", brand)

# # 🌟 Exercise 4 : Some Geography
# # Goal: Create a function that describes a city and its country.

# # Key Python Topics:

# # Functions with multiple parameters
# # Default parameter values
# # String formatting


# # Step 1: Define a Function with Parameters

# # Define a function named describe_city().
# # This function should accept two parameters: city and country.
# # Give the country parameter a default value, such as “Unknown”.


# # Step 2: Print a Message

# # Inside the function, set up the code to display a sentence like “ is in “.
# # Replace <city> and <country> with the parameter values.


# # Step 3: Call the Function

# # Call the describe_city() function with different city and country combinations.
# # Try calling it with and without providing the country argument to see the default value in action.
# # Example: describe_city("Reykjavik", "Iceland") and describe_city("Paris").


# # Expected Output:

# # Reykjavik is in Iceland.
# # Paris is in Unknown.

# def describe_city(city, country="Unknown"):
#     print(f"{city} is in {country}.")


# describe_city("Reykjavik", "Iceland")
# describe_city("Paris")



# import random

# def generate_random_number(number_1):
#     number_2 = random.randint(1, 100)

#     if number_1 == number_2:
#         print("Success!")
#     else:
#         print(f"Failed! Your number: {number_1}, Random number: {number_2}")

# generate_random_number(50)


# # 🌟 Exercise 6 : Let’s create some personalized shirts !
# # Goal: Create a function to describe a shirt’s size and message, with default values.

# # Key Python Topics:

# # Functions with parameters and default values
# # Keyword arguments


# # Step 1: Define a Function with Parameters

# # Define a function called make_shirt().
# # This function should accept two parameters: size and text.


# # Step 2: Print a Summary Message

# # Set up the function to display a sentence summarizing the shirt’s size and message.


# # Step 3: Call the Function



# # Step 4: Modify the Function with Default Values

# # Modify the make_shirt() function so that size has a default value of “large” and text has a default value of “I love Python”.


# # Step 5: Call the Function with Default and Custom Values

# # Call make_shirt() to make a large shirt with the default message.
# # Call make_shirt() to make a medium shirt with the default message.
# # Call make_shirt() to make a shirt of any size with a different message.


# # Step 6 (Bonus): Keyword Arguments

# # Call make_shirt() using keyword arguments (e.g., make_shirt(size="small", text="Hello!")).


# # Expected Output:

# # The size of the shirt is large and the text is I love Python.
# # The size of the shirt is medium and the text is I love Python.
# # The size of the shirt is small and the text is Custom message.

# def make_shirt(size, text):
#     print(f"The shirt size is {size} and the message is '{text}'.")
    
# make_shirt("M", "I love Basketball")

# #Step 4
# def make_shirt(size="large", text="I love Python"):
#     print(f"The shirt size is {size} and the message is '{text}'.")

# make_shirt()
# make_shirt(size="medium")
# make_shirt(text="I love JavaScript")

# make_shirt(size="small", text="Hello!")



# 🌟 Exercise 7 : Temperature Advice
# Goal: Generate a random temperature and provide advice based on the temperature range.

# Key Python Topics:

# Functions
# Conditionals (if / elif)
# Random numbers
# Floating-point numbers (Bonus)
# Handling seasons (Bonus)


# Step 1: Create the get_random_temp() Function

# Create a function called get_random_temp() that returns a random integer between -10 and 40 degrees Celsius.


# Step 2: Create the main() Function

# Create a function called main(). Inside this function:
# Call get_random_temp() to get a random temperature.
# Store the temperature in a variable and print a friendly message like:
# “The temperature right now is 32 degrees Celsius.”


# Step 3: Provide Temperature-Based Advice

# Inside main(), provide advice based on the temperature:
# Below 0°C: e.g., “Brrr, that’s freezing! Wear some extra layers today.”
# Between 0°C and 16°C: e.g., “Quite chilly! Don’t forget your coat.”
# Between 16°C and 23°C: e.g., “Nice weather.”
# Between 24°C and 32°C: e.g., “A bit warm, stay hydrated.”
# Between 32°C and 40°C: e.g., “It’s really hot! Stay cool.”


# Step 4: Floating-Point Temperatures (Bonus)

# Modify get_random_temp() to return a random floating-point number using random.uniform() for more accurate temperature values.


# Step 5: Month-Based Seasons (Bonus)

# Instead of directly generating a random temperature, ask the user for a month (1-12) and determine the season using if/elif conditions.
# Modify get_random_temp() to return temperatures specific to each season.


# Expected Output:

# The temperature right now is 32 degrees Celsius.
# It's really hot! Stay cool.


# import random

# def get_random_temp():
#     return random.randint(-10, 40)

# def main():
#     temp = get_random_temp()
#     if temp < 0:
#         print("Brrr, that’s freezing! Wear some extra layers today.")
#     elif 0 <= temp < 16:
#         print("Quite chilly! Don’t forget your coat.")
#     elif 16 <= temp < 23:
#         print("Nice weather.")
#     elif 24 <= temp < 32:
#         print("A bit warm, stay hydrated.")
#     elif 32 <= temp < 40:
#         print("It’s really hot! Stay cool.")


# #Bonus
# import random

# def get_random_temp(month):

#     # Winter
#     if month in [12, 1, 2]:
#         return random.randint(-10, 16)

#     # Spring
#     elif month in [3, 4, 5]:
#         return random.randint(10, 23)

#     # Summer
#     elif month in [6, 7, 8]:
#         return random.randint(24, 40)

#     # Autumn
#     else:
#         return random.randint(0, 20)


# def main():

#     month = int(input("Enter a month (1-12): "))

#     temp = get_random_temp(month)

#     print(f"The current temperature is {temp}°C.")

#     if temp < 0:
#         print("Brrr, that’s freezing! Wear some extra layers today.")

#     elif 0 <= temp < 16:
#         print("Quite chilly! Don’t forget your coat.")

#     elif 16 <= temp < 23:
#         print("Nice weather.")

#     elif 24 <= temp < 32:
#         print("A bit warm, stay hydrated.")

#     elif 32 <= temp < 40:
#         print("It’s really hot! Stay cool.")


# main()


# 🌟 Exercise 8: Pizza Toppings
# Key Python Topics:

# Loops
# Lists
# String formatting


# Instructions:

# Write a loop that asks the user to enter pizza toppings one by one.
# Stop the loop when the user types 'quit'.
# For each topping entered, print:
# "Adding [topping] to your pizza."
# After exiting the loop, print all the toppings and the total cost of the pizza.
# The base price is $10, and each topping adds $2.50.


# toppings = []
# total = 10

# while True:

#     topping = input("Enter a pizza topping (or type 'quit' to finish): ")

#     if topping.lower() == "quit":
#         break

#     toppings.append(topping)

#     total += 2.50

#     print(f"Adding {topping} to your pizza.")

# print("\nYour pizza toppings are:")

# for topping in toppings:
#     print(f"- {topping}")

# print(f"\nTotal price: ${total}")



items_purchase = {
    "Water": "$1",
    "Bread": "$3",
    "TV": "$1,000",
    "Fertilizer": "$20"
}

wallet = "$300"

wallet_value = int(wallet.replace("$", "").replace(",", ""))

basket = []

# Loop through the dictionary
for item, price in items_purchase.items():

    # Clean and convert the price
    price_value = int(price.replace("$", "").replace(",", ""))

    # Check if the item is affordable
    if price_value <= wallet_value:

        # Add item to basket
        basket.append(item)

        # Update wallet
        wallet_value -= price_value

# Final result
if len(basket) == 0:
    print("Nothing")

else:
    print(sorted(basket))
        
