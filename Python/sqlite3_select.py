import sqlite3


try:
    connection = sqlite3.connect('sqlite3.db')
    cursor = connection.cursor()

    cursor = connection.execute("SELECT * from STUDENT ORDER BY ADVISORID")
    
    print("\ndisplay all data..................\n")

    for row in cursor:
        print(row)
 
    print("\nretrieve with where clause..................\n")

    # WHERE CLAUSE TO RETRIEVE DATA
    stetement = "SELECT * FROM STUDENT WHERE STUDENTID >= 506 "
    result = cursor.execute(stetement)

    # printing the cursor data
    print(result.fetchall())

    print("\nretrieve with INNER JOIN..................\n")
    
    # Query for INNER JOIN 
    sql = '''
        SELECT StudentID, StudentName, AdvisorName  
        FROM STUDENT  
        INNER JOIN Advisor 
        ON Student.AdvisorID = Advisor.AdvisorID;
        '''
  
    # Executing the query 
    result = cursor.execute(sql) 
  
    # Fetching rows from the result table 
    result = result.fetchall() 
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
