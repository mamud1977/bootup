# The filter() function in Python 
# constructs an iterator 
# from elements of an iterable 
# for which the function returns true.

# # Syntax
# filter(function, iterable)

# Example
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Filter even numbers
even_numbers = filter(lambda x: x % 2 == 0, numbers)
print(list(even_numbers))  # Output: [2, 4, 6, 8, 10]

# Filter odd numbers
odd_numbers = filter(lambda x: x % 2 != 0, numbers)
print(list(odd_numbers))  # Output: [1, 3, 5, 7, 9]