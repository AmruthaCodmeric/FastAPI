from Basicprogram.inheritance import Animal


class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)   # Call parent constructor
        self.breed = breed       # Child variable

    def bark(self):              # Child method
        print(self.name, "is barking")


# Create object
dog1 = Dog("Buddy", "Labrador")

# Access variables
print("Name:", dog1.name)
print("Breed:", dog1.breed)

# Call methods
dog1.eat()     # Inherited method
dog1.bark()    # Child method