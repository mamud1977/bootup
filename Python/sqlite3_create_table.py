import sqlite3


try:
    connection = sqlite3.connect('sqlite3.db')
    cursor = connection.cursor()
     


    table ="""
        CREATE TABLE IF NOT EXISTS user
        (
        username VARCHAR(255), 
        password VARCHAR(255), 
        emailid VARCHAR(255)
        );
        """
    
    cursor.execute(table)


    # query to create a table named FOOD1
    table ="""
        CREATE TABLE IF NOT EXISTS EVENT
        (
        EVENTID VARCHAR(255), 
        EVENTNAME VARCHAR(255), 
        ORGANIZER  VARCHAR(255),
        YEAR    INT
        );
        """
    
    cursor.execute(table)
 

    # Create and populate tables 
    cursor.executescript(''' 
    CREATE TABLE IF NOT EXISTS Advisor( 
    AdvisorID INTEGER NOT NULL, 
    AdvisorName TEXT NOT NULL, 
    PRIMARY KEY(AdvisorID) 
    ); 
    
    CREATE TABLE IF NOT EXISTS STUDENT( 
    StudentID NUMERIC NOT NULL, 
    StudentName NUMERIC NOT NULL, 
    AdvisorID INTEGER, 
    FOREIGN KEY(AdvisorID) REFERENCES Advisor(AdvisorID), 
    PRIMARY KEY(StudentID) 
    ); 
                         
    ''') 
    
# Handle errors
except sqlite3.Error as error:
    print('Error occurred - ', error)
 
# Close DB Connection irrespective of success
# or failure
finally:
   
    if connection:
        connection.close()
        print('SQLite Connection closed')
