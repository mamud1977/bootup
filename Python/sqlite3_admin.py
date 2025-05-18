import sqlite3


try:
    connection = sqlite3.connect('sqlite3.db')
    cursor = connection.cursor()

    print('\nList all tables in the DB...\n') 

    sql = '''
        SELECT * FROM sqlite_master WHERE type='table'; 
        '''
    
    result = cursor.execute(sql) 
    
    for row in result: 
        print(row) 

    


# Handle errors
except sqlite3.Error as error:
    print('Error occurred - ', error)
 
# Close DB Connection irrespective of success
# or failure
finally:
   
    if connection:
        connection.close()
        print('SQLite Connection closed')
