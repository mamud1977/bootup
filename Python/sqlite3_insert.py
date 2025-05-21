import sqlite3


try:
    connection = sqlite3.connect('sqlite3.db')
    cursor = connection.cursor()
  
    # Queries to INSERT records. 
    # cursor.execute('''INSERT INTO STUDENT VALUES ('Raju', '7th', 'A')''') 
    # cursor.execute('''INSERT INTO STUDENT VALUES ('Shyam', '8th', 'B')''') 
    # cursor.execute('''INSERT INTO STUDENT VALUES ('Baburao', '9th', 'C')''') 
    # cursor.execute('''INSERT INTO STUDENT VALUES ('Zeenat', '7th', 'C')''') 

    connection.commit() 
  
    print("..................\n")


    # Create and populate tables 
    cursor.executescript(''' 
    
    INSERT INTO Advisor(AdvisorID, AdvisorName) VALUES 
    (1,"John Paul"),  
    (2,"Anthony Roy"),  
    (3,"Raj Shetty"), 
    (4,"Sam Reeds"), 
    (5,"Arthur Clintwood"); 
    
    INSERT INTO Student(StudentID, StudentName, AdvisorID) VALUES 
    (501,"Geek1",1), 
    (502,"Geek2",1), 
    (503,"Geek3",3), 
    (504,"Geek4",2), 
    (505,"Geek5",4), 
    (506,"Geek6",2), 
    (507,"Geek7",2), 
    (508,"Geek8",3), 
    (509,"Geek9",NULL), 
    (510,"Geek10",1); 
        
    ''') 
    
    connection.commit() 

# Handle errors
except sqlite3.Error as error:
    print('Error occurred - ', error)
 
# Close DB Connection irrespective of success
# or failure
finally:
   
    if connection:
        connection.close()
        print('SQLite Connection closed')
