def example_function(*argsmmmmm, **kwargsyyyy):
    print(type(argsmmmmm))
    print(type(kwargsyyyy))
    print("Positional arguments (args):", argsmmmmm)
    
    print("Keyword arguments (kwargs):", kwargsyyyy)

example_function(1, 2, 3, name="Abrar", age=13)
example_function(10, 20, 30, 40, name="Mamud", age=47, height=169)