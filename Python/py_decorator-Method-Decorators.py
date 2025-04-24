# A simple decorator function
def decorator(func):
  
    def wrapper():
        print("Before calling the function.")
        func()
        print("After calling the function.")
    return wrapper

# Applying the decorator to a function
# The @decorator syntax is a shorthand for greet = decorator(greet)

@decorator
def greet():
    print("Hello, World!")

greet()