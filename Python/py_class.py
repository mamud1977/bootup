class Animal:
    def __init__(self, name):
      
      	# Storing the name of the animal
        self.name = name  

    def sound(self):
      
        # This method should be implemented by subclasses
        raise NotImplementedError("Subclasses must implement this method")

class Dog(Animal):
    # Class variable
    species = "Canine"

    def __init__(self, name, age):
        # Instance variables
        self.name = name
        self.age = age

    def bark(self): 
        print(f"{self.name} is barking!")

    def sound(self):
      
        # Dog-specific sound
        return "Woof!"
    
    def __str__(self):
        return f"{self.name} is {self.age} years old."  # Correct: Returning a string
      


# Creating instances
# Animal instance with generic name
a = Animal("Generic Animal")  
print(a.name)  # Output: Generic Animal

print("...............\n")

# Creating an object 
dog1 = Dog("Buddy", 3)
dog2 = Dog("Tommy", 7)

print(dog1.name)  
print(dog1.age)  
print(dog1.species)
print(dog1.sound())  # Output: Woof!
dog1.bark()
print(dog1) 

print("...............\n")

print(dog2.name)  
print(dog2.age)  
print(dog2.species)
dog2.bark()
print(dog2) 

print("...............\n")

print("\nDictionary form :", vars(dog1))
print("\ndir(dog1):",dir(dog1))
print("\ndog1.__module__:",dog1.__module__)




 
