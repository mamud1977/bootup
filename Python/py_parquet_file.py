import pandas as pd
import random

# Generate a 6-digit random number
random_number = random.randint(100000, 999999)

# Create a DataFrame
df = pd.DataFrame({"random_6_digit": [random_number]})

# Save to Parquet
df.to_parquet("random_number.parquet", index=False)

print(f"Generated Parquet file with number: {random_number}")
