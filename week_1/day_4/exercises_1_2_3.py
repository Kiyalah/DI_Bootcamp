# 🌟 Exercise 1: Pets
# Key Python Topics:

# Inheritance
# Class instantiation
# Lists
# Polymorphism


# Instructions:

# Use the provided Pets and Cat classes to create a Siamese breed, instantiate cat objects, and use the Pets class to manage them.
# See the example below, before diving in.



# Step 1: Create the Siamese Class

# Create a class called Siamese that inherits from the Cat class.
# You can add any specific attributes or methods for the Siamese breed, or leave it as is if there are no unique behaviors.


# Step 2: Create a List of Cat Instances

# Create a list called all_cats that contains instances of Bengal, Chartreux, and Siamese cats.
# Example: all_cats = [bengal_obj, chartreux_obj, siamese_obj]
# Give each cat a name and age.


# Step 3: Create a Pets Instance

# Create an instance of the Pets class called sara_pets, passing the all_cats list as an argument.


# Step 4: Take Cats for a Walk

# Call the walk() method on the sara_pets instance.
# This should print the result of calling the walk() method on each cat in the list.



# Step 1: Create the Siamese class

# Step 2: Create a list of cat instances

# Step 3: Create a Pets instance of the list of cat instances

# sara_pets = Pets(all_cats)

# Step 4: Take cats for a walk
# sara_pets.walk()


class Pets():
    def __init__(self, animals):
        self.animals = animals

    def walk(self):
        for animal in self.animals:
            print(animal.walk())

class Cat():
    is_lazy = True

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def walk(self):
        return f'{self.name} is just walking around'

class Bengal(Cat):
    def sing(self, sounds):
        return f'{sounds}'

class Chartreux(Cat):
    def sing(self, sounds):
        return f'{sounds}'
    

class Siamese(Cat):
    def sing(self, sounds):
        return f'{sounds}'
    
all_cats = [bengal_obj, chartreux_obj, siamese_obj] = Bengal('Mione', 3), Chartreux('Mitwo', 5), Siamese('Mithree', 2)


print(bengal_obj.walk())
print(chartreux_obj.walk())
print(siamese_obj.walk())

sara_pets = Pets(all_cats)
sara_pets.walk()


# 🌟 Exercise 2: Dogs
# Goal: Create a Dog class with methods for barking, running speed, and fighting.



# Key Python Topics:

# Classes and objects
# Methods
# Attributes


# Instructions:

# Step 1: Create the Dog Class

# Create a class called Dog with name, age, and weight attributes.
# Implement a bark() method that returns “<dog_name> is barking”.
# Implement a run_speed() method that returns weight / age * 10.
# Implement a fight(other_dog) method that returns a string indicating which dog won the fight, based on run_speed * weight.


# Step 2: Create Dog Instances

# Create three instances of the Dog class with different names, ages, and weights.


# Step 3: Test Dog Methods

# Call the bark(), run_speed(), and fight() methods on the dog instances to test their functionality.


class Dog():
    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight
        
    def bark(self):
        return f"{self.name} is barking"
    
    def run_speed(self):
        return self.weight / self.age * 10

    def fight(self, other_dog):
        if self.run_speed() > other_dog.run_speed():
            return f"{self.name} wins the fight!"
        elif self.run_speed() < other_dog.run_speed():
            return f"{other_dog.name} wins the fight!"
        else:
            return "It's a tie!"
        
        
Lassi = Dog("Lassi", 5, 20)
Rex = Dog("Rex", 3, 15)
Zigs = Dog("Zigs", 4, 25)

print(Lassi.bark())
print(Rex.run_speed())
print(Lassi.fight(Rex))


# 🌟 Exercise 3: Dogs Domesticated
# Goal: Create a PetDog class that inherits from Dog and adds training and tricks.



# Key Python Topics:

# Inheritance
# super() function
# *args
# Random module


# Instructions:

# Step 1: Import the Dog Class

# In a new Python file, import the Dog class from the previous exercise.


# Step 2: Create the PetDog Class

# Create a class called PetDog that inherits from the Dog class.
# Add a trained attribute to the __init__ method, with a default value of False.
# trained means that the dog is trained to do some tricks.
# Implement a train() method that prints the output of bark() and sets trained to True.
# Implement a play(*args) method that prints “<dog_names> all play together”.
# *args on this method is a list of dog instances.
# Implement a do_a_trick() method that prints a random trick if trained is True.
# Use this list for the ramdom tricks:
# tricks = ["does a barrel roll", "stands on his back legs", "shakes your hand", "plays dead"]
# Choose a random index from it each time the method is called.


# Step 3: Test PetDog Methods

# Create instances of the PetDog class and test the train(), play(*args), and do_a_trick() methods.

import random

class PetDog(Dog):
    def __init__(self, name, age, weight, owner, trained=False):
        super().__init__(name, age, weight)
        self.owner = owner
        self.trained = trained

    def greet_owner(self):
        return f"{self.name} greets {self.owner}!"
    
    def train(self):
        self.trained = True
        print(f"{self.bark()} is now trained.")
        
    def play(*dogs):
        tricks = ["does a barrel roll", "stands on his back legs", "shakes your hand", "plays dead"]
        for dog in dogs:
            trick = random.choice(tricks)
            print(f"{dog.name} : {trick}!")
            
            
my_pet_dog = PetDog("Buddy", 4, 20, "Alice")
print(my_pet_dog.greet_owner())
my_pet_dog.train()

my_pet_dog.play(Lassi, Rex, Zigs)
