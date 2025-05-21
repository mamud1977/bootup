import sqlite3


try:
    connection = sqlite3.connect('sqlite3.db')
    cursor = connection.cursor()
    print('DB Init')

    # Write a query and execute it with cursor
    query = 'select sqlite_version();'
    cursor.execute(query)
    
    # Fetch and output result
    result = cursor.fetchall()
    print(f'SQLite Version is {result}')

    
# Handle errors
except sqlite3.Error as error:
    print('Error occurred - ', error)
 
# Close DB Connection irrespective of success
# or failure
finally:
   
    if connection:
        connection.close()
        print('SQLite Connection closed')
