# Instructions
# The goal is to create a class that represents a simple circle.

# A Circle can be defined by either specifying the radius or the diameter - use a decorator for it.
# The user can query the circle for either its radius or diameter.



# Abilities of a Circle Instance
# Your Circle class should be able to:

# ✅ Compute the circle’s area.
# ✅ Print the attributes of the circle — use a dunder method (__str__ or __repr__).
# ✅ Add two circles together and return a new circle with the new radius — use a dunder method (__add__).
# ✅ Compare two circles to see which is bigger — use a dunder method (__gt__).
# ✅ Compare two circles to check if they are equal — use a dunder method (__eq__).
# ✅ Store multiple circles in a list and sort them — implement __lt__ or other comparison methods.


# Bonus Challenge (Optional)
# If you want an extra challenge:

# Install the Turtle module (pip install PythonTurtle)
# Draw the sorted circles visually on the screen!


# 💡 Tip:

# Test your implementation by creating several circles and printing comparisons, additions, and sorted results.

import math


class Circle:

    # Initialize the circle with a radius
    def __init__(self, radius):
        self.radius = radius


    # Decorator to get the diameter
    @property
    def diameter(self):
        return self.radius * 2


    # Decorator to set the diameter
    @diameter.setter
    def diameter(self, value):
        self.radius = value / 2


    # Calculate the area of the circle
    def area(self):
        return math.pi * (self.radius ** 2)


    # Display the object in a readable format
    def __str__(self):
        return (
            f"Circle(radius={self.radius}, "
            f"diameter={self.diameter:.2f}, "
            f"area={self.area():.2f})"
        )


    # Add two circles together
    # Return a new Circle object
    def __add__(self, other_circle):

        new_radius = self.radius + other_circle.radius

        return Circle(new_radius)


    # Compare if one circle is bigger than another
    def __gt__(self, other_circle):

        return self.radius > other_circle.radius


    # Compare if two circles are equal
    def __eq__(self, other_circle):

        return self.radius == other_circle.radius


    # Allow sorting of circles with sorted()
    def __lt__(self, other_circle):

        return self.radius < other_circle.radius



# Create circle objects
circle1 = Circle(5)
circle2 = Circle(10)
circle3 = Circle(7)


# Print circles
print(circle1)
print(circle2)
print(circle3)


# Check the diameter
print(circle1.diameter)


# Modify the diameter
circle1.diameter = 20

print(circle1)


# Calculate the area
print(circle2.area())


# Add two circles
new_circle = circle1 + circle2

print(new_circle)


# Compare circles
print(circle2 > circle3)

print(circle1 == circle2)


# Sort circles
circles = [circle1, circle2, circle3]

sorted_circles = sorted(circles)

print("\nSorted Circles:")

for circle in sorted_circles:
    print(circle)