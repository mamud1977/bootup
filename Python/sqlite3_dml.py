import sqlite3

class my_sqlite3_db:
    connection = sqlite3.connect('sqlite3.db')
    cursor = connection.cursor()


     

import sqlite3 as sql

def insertUser(username,password):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (username,password))
    con.commit()
    con.close()

def retrieveUsers():
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT username, password FROM users")
	users = cur.fetchall()
	con.close()
	return users