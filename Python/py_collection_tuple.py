# Built-in data types to store collections of data:

#   1. Tuple 
#   - immutable
#   - items cannot be updated, removeed, appended or extended.
 

v_tuple = ("a","b","c", 1,1,3,"Apple")

print(v_tuple)
print("v_tuple.count: ", v_tuple.count(1))
print("v_tuple.index: ", v_tuple.index("Apple"))

print("Value in v_tuple[-1] = ", v_tuple[0])
print("Value in v_tuple[-1] = ", v_tuple[-1])

# v_tuple[1] = 100  --- > will throw error


print("\nTraverse through each item in the tuple")
for x in v_tuple:
    print(x, end=" ")
print("\n")

print("\nCode for concatenating 2 tuples")

tup1 = (0, 1, 2, 3)
tup2 = ('python', 'geek')
tup3 = tup1 + tup2

print(tup1 + tup2)
print(tup3)
print(type(tup3))

print("\ncode to test slicing")
print(v_tuple)
print(v_tuple[::-1])
print(v_tuple[2:4])


print("\nCode for converting a list and a string into a tuple")
a = [0, 1, 2]
tup = tuple(a)
print(tup)
print(type(tup))

b = (0, 1, 2)
lst = list(b)
print(lst)
print(type(lst))

# Creating a single-element tuple
tup = (10, )
print(tup) 
print(type(tup))

# What if we do not use comma
tup = (10) 
print(tup)  
print(type(tup))



# all()	Returns true if all element are true or if tuple is empty
# any()	return true if any element of the tuple is true. if tuple is empty, return false
# len()	Returns length of the tuple or size of the tuple
# enumerate()	Returns enumerate object of tuple
# max()	return maximum element of given tuple
# min()	return minimum element of given tuple
# sum()	Sums up the numbers in the tuple
# sorted()	input elements in the tuple and return a new sorted list
# tuple()	Convert an iterable to a tuple.

print("\nTuple Built-In Functions: all()")

tuple2 = (True, False, True)
print(all(tuple2))  # False

tuple3 = (1, 2, 3) # All non-zero numbers are considered True
print(all(tuple3))  # True

tuple4 = (0, 1, 2) # 0 is considered False
print(all(tuple4))  # False

tuple5 = () # Empty tuple
print(all(tuple5))  # True

print("\nTuple Built-In Functions: max()")
t = (1, 5, 2, 8, 3)
print(t)
max_value = max(t)
print(max_value)  # Output: 8
