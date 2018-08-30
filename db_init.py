import sqlite3
import os 

db_file = open('db.sqlite3','w+')
db_file.close()

db = sqlite3.connect('db.sqlite3')
db_cursor = db.cursor()

db_cursor.executescript('''
	CREATE TABLE posts(
		submission text, 
		comment text,
		created_at real
	);

	INSERT INTO posts 
	VALUES (
		'2maolz',
		'PLUS ULTRA',
		'1535602166.0'
	); 
''')


# check added values 
print(len(db_cursor.execute("SELECT * FROM posts").fetchall()))

# delete everything from the table 
db_cursor.execute("DELETE FROM posts") 

# check again
print(len(db_cursor.fetchall()))

# save and close 
db.commit()
db.close()
