# Python Lambda Functions are anonymous functions.
# They are the function without name
# The def keyword is used to define a normal function
# The lambda keyword is used to define an anonymous function 


s1 = 'GeeksforGeeks'
s2 = lambda func: func.upper()
print(s2(s1))

print('-------------------------------')

n = lambda x: "Positive" if x > 0 else "Negative" if x < 0 else "Zero"
print(n(5))   
print(n(-3))  
print(n(0))

print('-------------------------------')

list_comprehension = [lambda arg=x: arg * 10 for x in range(1, 5)]
for i in list_comprehension:
    print(i())


is_empty = lambda x: not x 
print(is_empty(None))        # Output: True
print(is_empty(""))          # Output: True
print(is_empty([]))          # Output: True
print(is_empty(0))           # Output: True
print(is_empty("hello"))     # Output: False
print(is_empty([1, 2, 3]))   # Output: False