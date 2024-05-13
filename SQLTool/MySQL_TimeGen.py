import numpy as np
from datetime import datetime, timedelta
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
table = 'ALiN'

# SQL query to check if data exists
check_query = """
SELECT DISTINCT DateTime FROM {} LIMIT 50 
"""

formatted_check_query = check_query.format(table)
cursor.execute(formatted_check_query)
result = cursor.fetchall()  # Fetch the count
#print(result)


# Closing the cursor and connection
cursor.close()
connection.close()


for dt in result:
    print(dt[0])
    final_time = dt[0] + timedelta(minutes = 5)
    # Generate evenly spaced DateTime values using linspace
    print(final_time)
    print('-'*50)
