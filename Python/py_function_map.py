v_list = [0,1,2,3,4,10,5,8,9,6,7]

def square(x):
    return x**2

results = map(square,v_list)

#print(list(results)) # Output: [1, 4, 9, 16]

for i,s in enumerate(results):
    print(v_list[i], s)