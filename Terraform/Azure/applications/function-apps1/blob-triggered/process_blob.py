import logging
import pyarrow.parquet as pq
import io

def main(myblob: bytes, name: str):
    logging.info(f"Triggered by blob: {name}")

    try:
        buffer = io.BytesIO(myblob)
        table = pq.read_table(buffer)
        df = table.to_pandas()

        logging.info(f"Loaded Parquet with {len(df)} rows and {len(df.columns)} columns")
        # Add your custom logic here

    except Exception as e:
        logging.error(f"Error processing Parquet file: {e}")
