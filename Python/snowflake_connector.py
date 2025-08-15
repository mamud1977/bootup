import snowflake.connector
import logging

if logging.getLogger().hasHandlers():
    # AWS Lambda Logger
    logging.getLogger().setLevel(logging.INFO)
else:
    # Local Logger
    logging.basicConfig(
        format="%(name)s: %(asctime)s - %(message)s",
        datefmt="%y-%d-%m %H:%M:%S",
        level=logging.INFO,
    )

# Replace with your Snowflake account details
account = "LRIIGSP-OO89314"
user = "Awstechlearn2"
password = "Password12345$"
warehouse = "COMPUTE_WH"
database = "AWSTESTDB"
schema = "AWSTESTSCHEMA"
role="accountadmin"

def connect():
    try:
        snowflake_connection = snowflake.connector.connect(
            user=user,
            account=account,
            #private_key=pkb,
            password=password,
            warehouse=warehouse,
            database=database,
            schema=schema,
            role=role,
            )

        logging.info("Successfully Connected to Snowflake.")
        return snowflake_connection
        
    except Exception:
        logging.exception("Unable to connect to Snowflake.")
        raise

if __name__ == "__main__":
    conn = connect();
    print(conn)
    cursor = conn.cursor()
    cursor.execute("SELECT CURRENT_DATE()")
    result = cursor.fetchone()
    print(f"Current Date: {result[0]}")
    cursor.close()
