# basic_classes.py
# Author: Nick Wlodychak
# Date: 23-09-24

"""
basic_classes.py defines classes for Circle and GraduateStudents and
returns their following attributes
"""

import math  # Importing the math module to use math.pi


class Circle:
    def __init__(self, color, radius):
        self.color = color
        self.radius = radius

    def diameter(self):
        return 2 * self.radius

    def circumference(self):
        return 2 * math.pi * self.radius

    def isRed(self):
        return self.color.lower() == "red"


class GraduateStudent:
    def __init__(self, first_name, last_name, year, major):
        self.first_name = first_name
        self.last_name = last_name
        self.year = year
        self.major = major

    def year_matriculated(self):
        current_year = 2020
        return current_year - self.year


# Testing Classes
circle1 = Circle("red", 2)
circle2 = Circle("blue", 13)
print(circle1.diameter())
print(circle1.circumference())
print(circle1.isRed())

print(circle2.diameter())
print(circle2.circumference())
print(circle2.isRed())

student1 = GraduateStudent("Nick", "Wlodychak", 1, "Biology")
student2 = GraduateStudent("Steven", "John", 5, "Bioinformatics")

print(student1.year_matriculated())
print(student2.year_matriculated())
