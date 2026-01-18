import os
import sys
import time
import pandas as pd
from sqlalchemy import create_engine

def main():
    url = os.environ.get("DATA_URL")
    if not url:
        print("ERROR: DATA_URL environment variable is required")
        sys.exit(1)

    database_url = os.environ.get(
        "DATABASE_URL",
        "postgresql://root:root@pgdatabase:5432/ny_taxi"
    )

    table_name = os.environ.get(
        "TARGET_TABLE",
        "yellow_taxi_trips_2021_1"
    )

    chunksize = int(os.environ.get("CHUNKSIZE", 100000))

    print("Starting ingestion with settings:")
    print(f"  DATA_URL     = {url}")
    print(f"  DATABASE_URL = {database_url}")
    print(f"  TABLE        = {table_name}")
    print(f"  CHUNKSIZE    = {chunksize}")

    engine = create_engine(database_url)

    df_iter = pd.read_csv(
        url,
        iterator=True,
        chunksize=chunksize
    )

    for i, df in enumerate(df_iter, start=1):
        start_time = time.time()

        df.to_sql(
            table_name,
            engine,
            if_exists="append",
            index=False
        )

        end_time = time.time()
        print(f"Chunk {i} loaded in {end_time - start_time:.2f} seconds")

    print("Ingestion completed successfully")

if __name__ == "__main__":
    main()
