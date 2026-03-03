import pandas as pd
import pyarrow
import fastparquet
from datetime import datetime, timedelta

base_time = datetime(2025, 9, 17, 10, 0)

for i in range(1, 6):
    po_number = f"PO-20250917-00{i}"
    data = []
    for j in range(1, 11):
        data.append({
            "PO_Number": po_number,
            "Test_ID": f"T{j:03}",
            "Test_Name": f"TestType{j}",
            "Result": "Pass" if j % 2 == 0 else "Fail",
            "Timestamp": (base_time + timedelta(minutes=5*j)).isoformat()
        })
    df = pd.DataFrame(data)
    df.to_csv(f"test_data_0{i}.txt", index=False)
    df.to_parquet(f"test_data_0{i}.parquet", index=False)
