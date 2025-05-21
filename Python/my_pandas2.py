import pandas as pd

df= pd.read_csv('/mnt/c/MyWork/gitlocal/bootup/sampleData/rainfall.csv')

print(df.columns)

df1 = df[['num', 'altitude','name', 'x_utm', 'y_utm']]
df2 = df[['num','sep','oct','nov','dec','jan','feb','mar','apr','may']]

print(df1.head(10))
print(df2.head(10))

print(df1.info())
print(df2.info())

filtered_df1 = df1[df1['num'] > 337000 ]   

print(f'filtered_df1: {filtered_df1}')


# Define a dictionary containing employee data
data1 = {'Name': ['Jai', 'Princi', 'Gaurav', 'Anuj'],
         'Age': [27, 24, 22, 32],
         'Address': ['Nagpur', 'Kanpur', 'Allahabad', 'Kannuaj'],
         'Qualification': ['Msc', 'MA', 'MCA', 'Phd'],
         'Mobile No': [97, 91, 58, 76]}

# Define a dictionary containing employee data
data2 = {'Name': ['Gaurav', 'Anuj', 'Dhiraj', 'Hitesh'],
         'Age': [22, 32, 12, 52],
         'Address': ['Allahabad', 'Kannuaj', 'Allahabad', 'Kannuaj'],
         'Qualification': ['MCA', 'Phd', 'Bcom', 'B.hons'],
         'Salary': [1000, 2000, 3000, 4000]}

# Convert the dictionary into DataFrame
df = pd.DataFrame(data1, index=[0, 1, 2, 3])

# Convert the dictionary into DataFrame
df1 = pd.DataFrame(data2, index=[2, 3, 6, 7])

print(df, "\n\n", df1)

res2 = pd.concat([df, df1], axis=1, join='inner')

print(f'inner join:\n {res2}')

res2 = pd.concat([df, df1],  axis=1, sort=False)

print(f'union of dataframe:\n {res2}')

# -----------------------------------

# Define a dictionary containing employee data
data1 = {'Name': ['Jai', 'Princi', 'Gaurav', 'Anuj'],
         'Age': [27, 24, 22, 32],
         'Address': ['Nagpur', 'Kanpur', 'Allahabad', 'Kannuaj'],
         'Qualification': ['Msc', 'MA', 'MCA', 'Phd']}

# Define a dictionary containing employee data
data2 = {'Name': ['Abhi', 'Ayushi', 'Dhiraj', 'Hitesh'],
         'Age': [17, 14, 12, 52],
         'Address': ['Nagpur', 'Kanpur', 'Allahabad', 'Kannuaj'],
         'Qualification': ['Btech', 'B.A', 'Bcom', 'B.hons']}

# Convert the dictionary into DataFrame
df = pd.DataFrame(data1, index=[0, 1, 2, 3])

# Convert the dictionary into DataFrame
df1 = pd.DataFrame(data2, index=[4, 5, 6, 7])

print(df, "\n\n", df1)

res = df.append(df1)
print(f"append:\n", res)