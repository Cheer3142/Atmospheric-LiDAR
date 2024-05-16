import mysql.connector

# Establishing connection to MySQL
connection = mysql.connector.connect(
    host="192.168.2.190",
    port="1890",
    user="root",
    password="Cheer123",
    database="Cheer"
)

# Creating a cursor object
cursor = connection.cursor()
db = 'ALiN'

# SQL query to delete all rows from a table
delete_all_query = """
DELETE FROM %s
""" % db

# SQL query to delete specific rows based on a condition
delete_query = """
DELETE FROM %s 
WHERE DateTime BETWEEN '2024-05-14 10:00:00' AND '2024-05-15 12:00:00'
""" % db

reset_auto_increment_query = """
ALTER TABLE %s AUTO_INCREMENT = 1
""" % db

# Executing the SQL query to delete all rows
cursor.execute(delete_query)
#cursor.execute(reset_auto_increment_query)

# Committing the changes
connection.commit()

# Closing the cursor and connection
cursor.close()
connection.close()
