import sqlite3
connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()
command = """CREATE TABLE IF NOT EXISTS admin(name TEXT, password TEXT)"""
cursor.execute(command)
username = 'admin'
password = 'admin'
cursor.execute("insert into admin values('"+username+"', '"+password+"')")
connection.commit()