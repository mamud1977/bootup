
print('Write a function that reverses a string. ------------------------')

s = ["H","a","n","n","a","h"]
print(s)
l = len(s)
s_new = []
for i,c in enumerate(s):
    s_new.append(s[l-i-1])

print(s_new)


print('highest_non_repeating number ------------------------')

nums1 = [4, 8, 5, 1, 2, 4, 3, 8, 3] # Output: 5
print(nums1)
nums1.sort(reverse=True)
print(nums1)

for i, n in enumerate(nums1):
    if nums1.count(n) ==  1:
        print(n )
        break
    





