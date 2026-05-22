# # class Pets():
# #     def __init__(self, animals):
# #         self.animals = animals

# #     def walk(self):
# #         for animal in self.animals:
# #             print(animal.walk())

# # class Cat():
# #     is_lazy = True

# #     def __init__(self, name, age):
# #         self.name = name
# #         self.age = age

# #     def walk(self):
# #         return f'{self.name} is just walking around'

# # class Bengal(Cat):
# #     def sing(self, sounds):
# #         return f'{sounds}'

# # class Chartreux(Cat):
# #     def sing(self, sounds):
# #         return f'{sounds}'
    

# # class Siamese(Cat):
# #     def sing(self, sounds):
# #         return f'{sounds}'
    
# # all_cats = [bengal_obj, chartreux_obj, siamese_obj] = Bengal('Mione', 3), Chartreux('Mitwo', 5), Siamese('Mithree', 2)


# # print(bengal_obj.walk())
# # print(chartreux_obj.walk())
# # print(siamese_obj.walk())

# # sara_pets = Pets(all_cats)
# # sara_pets.walk()


# class Dog():
#     def __init__(self, name, age, weight):
#         self.name = name
#         self.age = age
#         self.weight = weight
        
#     def bark(self):
#         return f"{self.name} is barking"
    
#     def run_speed(self):
#         return self.weight / self.age * 10

#     def fight(self, other_dog):
#         if self.run_speed() > other_dog.run_speed():
#             return f"{self.name} wins the fight!"
#         elif self.run_speed() < other_dog.run_speed():
#             return f"{other_dog.name} wins the fight!"
#         else:
#             return "It's a tie!"
        
        
# Lassi = Dog("Lassi", 5, 35)
# Rex = Dog("Rex", 3, 15)
# Zigs = Dog("Zigs", 4, 25)

# print(Lassi.bark())
# print(Rex.run_speed())
# print(Lassi.fight(Rex))


# class Dog():
#     def __init__(self, name, age, weight):
#         self.name = name
#         self.age = age
#         self.weight = weight
        
#     def bark(self):
#         return f"{self.name} is barking"
    
#     def run_speed(self):
#         return self.weight / self.age * 10

#     def fight(self, other_dog):
#         if self.run_speed() > other_dog.run_speed():
#             return f"{self.name} wins the fight!"
#         elif self.run_speed() < other_dog.run_speed():
#             return f"{other_dog.name} wins the fight!"
#         else:
#             return "It's a tie!"
        
        
# Lassi = Dog("Lassi", 5, 20)
# Rex = Dog("Rex", 3, 15)
# Zigs = Dog("Zigs", 4, 25)

# print(Lassi.bark())
# print(Rex.run_speed())
# print(Lassi.fight(Rex))



# import random

# class PetDog(Dog):
#     def __init__(self, name, age, weight, owner, trained=False):
#         super().__init__(name, age, weight)
#         self.owner = owner
#         self.trained = trained

#     def greet_owner(self):
#         return f"{self.name} greets {self.owner}!"
    
#     def train(self):
#         self.trained = True
#         print(f"{self.bark()} is now trained.")
        
#     def play(*dogs):
#         tricks = ["does a barrel roll", "stands on his back legs", "shakes your hand", "plays dead"]
#         for dog in dogs:
#             trick = random.choice(tricks)
#             print(f"{dog.name} : {trick}!")
            
            
# my_pet_dog = PetDog("Buddy", 4, 20, "Alice")
# print(my_pet_dog.greet_owner())
# my_pet_dog.train()

# my_pet_dog.play(Lassi, Rex, Zigs)

# 🌟 Exercise 4: Family and Person Classes
# Goal:

# Practice working with classes and object interactions by modeling a family and its members.



# Key Python Topics:

# Classes and objects
# Instance methods
# Object interaction
# Lists and loops
# Conditional statements (if/else)
# String formatting (f-strings)


# Instructions:

# Step 1: Create the Person Class

# Define a Person class with the following attributes:
# first_name
# age
# last_name (string, should be initialized as an empty string)
# Add a method called is_18():
# It should return True if the person is 18 or older, otherwise False.


# Step 2: Create the Family Class

# Define a Family class with:
# A last_name attribute
# A members list that will store Person objects (should be initialized as an empty list)


# Add a method called born(first_name, age):
# It should create a new Person object with the given first name and age.
# It should assign the family’s last name to the person.
# It should add this new person to the members list.


# Add a method called check_majority(first_name):
# It should search the members list for a person with that first_name.
# If the person exists, call their is_18() method.
# If the person is over 18, print:
# "You are over 18, your parents Jane and John accept that you will go out with your friends"
# Otherwise, print:
# "Sorry, you are not allowed to go out with your friends."


# Add a method called family_presentation():
# It should print the family’s last name.
# Then, it should print each family member’s first name and age.


# Expected Behavior:

# Once implemented, your program should allow you to:

# Create a family with a last name.
# Add members to the family using the born() method.
# Use check_majority() to see if someone is allowed to go out.
# Display family information with family_presentation().
# Don’t forget to test your classes by creating an instance of Family, adding members, and calling each method to see the expected output.

class Person:
    def __init__(self, first_name, age, last_name):
        self.first_name = first_name
        self.age = age
        self.last_name = last_name

    def is_18(self):
        return self.age >= 18


class Family:
    def __init__(self, last_name):
        self.last_name = last_name
        self.members = []
        
    def born(self, first_name, age):
        new_member = Person(first_name, age, self.last_name)
        self.members.append(new_member)

    def check_majority(self, first_name):
        for member in self.members:
            if member.first_name == first_name:
                if member.is_18():
                    print(f"You are over 18, your parents {self.last_name} accept that you will go out with your friends")
                else:
                    print("Sorry, you are not allowed to go out with your friends.")
                return
        print("Person not found in the family.")

    def family_presentation(self):
        print(f"Family Name: {self.last_name}")
        for member in self.members:
            print(f"Member: {member.first_name}, Age: {member.age}")


Family1 = Family("Smith")
Family1.born("Alice", 20)
Family1.born("Bob", 15)
Family1.check_majority("Alice")
Family1.check_majority("Bob")
Family1.family_presentation()