import pyarrow.parquet as pq
import pandas as pd

table = pq.read_table('/mnt/c/MyWork/gitlocal/bootup/SampleData/iris.parquet')
print(table)
print(table.shape)

df = table.to_pandas()
# Taking tanspose so the printing dataset will easy.
print(df)

df['new_col'] = 'new_col'

df.to_parquet('/mnt/c/MyWork/gitlocal/bootup/SampleData/iris_new.parquet')

df = pd.read_parquet('/mnt/c/MyWork/gitlocal/bootup/SampleData/iris.parquet')
df2 = df['variety'].head(100)

print(df2)
