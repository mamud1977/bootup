import sqlite3


try:
    connection = sqlite3.connect('sqlite3.db')
    cursor = connection.cursor()

    sql = '''
        SELECT * FROM STUDENT  
        '''
  
    # Executing the query 
    result = cursor.execute(sql) 
    
    print('\nBefore Update...\n') 
    for row in result: 
        print(row) 

    # Updating 
    cursor.execute('''
                   UPDATE STUDENT SET ADVISORID = 5 WHERE ADVISORID=4;
                   ''') 
    
    print(f'total_changes = {connection.total_changes}\n')
    print('\nAfter Update...\n') 

    sql = '''
        SELECT * FROM STUDENT  
        '''
  
    # Executing the query 
    result = cursor.execute(sql) 
    
    print('\nBefore Update...\n') 
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
