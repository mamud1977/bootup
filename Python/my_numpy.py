import numpy as np



print(f'\nNumpy Array: .......................')

lst = [107,267,39,545,444]

arr = np.array(lst)
print(f'numpy array: {arr}')

print(f'numpy array - max element: {arr.max()}')



print(f'\nRandum numbers: .......................')

# Generate a single random integer 
# between 0 (inclusive) and 10 (exclusive)


random_int = np.random.randint(7.7)
print(f'random_int:{random_int}')

# Generate an array of 5 random integers 
# between 1 (inclusive) and 6 (exclusive)
random_array = np.random.randint(1, 6, 5)
print(random_array)

# Generate a 2x3 array of random integers 
# between -5 (inclusive) and 5 (exclusive)
random_matrix = np.random.randint(-5, 5, (4, 5))
print(random_matrix)

print(random_matrix.size)

random_matrix2 = random_matrix.reshape(5,4)
print(random_matrix2)

lst = [107,267,39,545,444]

arr = [[10,11,12,13],
       [14,15,16,17],
       [18,19,20,21],
       [22,23,24,25],
       [26,27,28,29]]
arr = np.array(arr)

print(arr)

print(arr[2,3])

print(arr[2,:])

print(arr[0:2,1:3])

print(f'\nRandum numbers aith numpy.arange: .......................')

# Create an array from 0 to 9
arr1 = np.arange(10)
print(arr1)  # Output: [0 1 2 3 4 5 6 7 8 9]

# Create an array from 1 to 10 with a step of 2
arr2 = np.arange(1, 21, 2)
print(arr2)  # Output: [1 3 5 7 9]

# Create an array from 0 to 1 with a step of 0.1
arr3 = np.arange(0, 1, 0.1)
print(arr3)  # Output: [0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9]

print(f'\nnp.zeros: .......................')
print(np.zeros((4,6)))

print(f'\nnp.linspace(0.0001,.9999,11): .......................')
print(np.linspace(0.01,0.99,11))