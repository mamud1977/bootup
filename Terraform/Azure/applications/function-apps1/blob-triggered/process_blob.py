import logging
import pyarrow.parquet as pq
import io
import azure.functions as func

def main(myblob: func.InputStream):
    logging.info(f"Blob trigger fired for: {myblob.name}")
    logging.info(f"Blob size: {myblob.length} bytes")