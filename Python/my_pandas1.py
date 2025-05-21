import pandas as pd


df= pd.read_csv('/mnt/c/MyWork/gitlocal/bootup/sampleData/census.csv')

print(f'read a CSV file into a Panda dataframe..............')
print(f'df1: {df.head(100)}')

print(f'select columns..............')

# df2 = df1[['name','salary','year']]

# print(f'list of columns:\n {list(df2.columns)}')
      
# print(df2.head(10))

# print(df2.dtypes)

# print(f'where condition..............')

# df3=df1.where(df1['year'] == 2015).dropna()
# print(df3)

# print(f'groupby..............')
# grp = df3.groupby(['year']).max('salary')

# # grp = df2.groupby(['term','issue_year']).max('loan_amnt')
# print(f'grp:\n {grp}')

# # print(f'.......................')
# # grp = df2.groupby(['term','issue_year'])
# # for name, group in grp:
# #     print(name)
# #     print(group)
# #     print()

df1= pd.read_csv('/mnt/c/MyWork/gitlocal/bootup/sampleData/census.csv')


