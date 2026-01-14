import sys
print("arguments", sys.argv)
import pandas as pd


month  = int(sys.argv[1])
print(f"Running pipeline for month  {month}")

df = pd.DataFrame({"day": [1, 2], "num_passagers": [3, 4]})
df['month'] = month  
print(df.head())

df.to_parquet(f"output_month={month}.parquet")
print(f'hello from pipeline for month {month}')