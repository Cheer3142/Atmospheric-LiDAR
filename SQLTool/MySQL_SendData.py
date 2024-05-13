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
# Sample data to insert
data_to_insert = [
    (table, 12.5, 2, '2024-04-03 20:35:00', '10:30:00'),
    (table, 13.5, 7, '2024-04-20 10:30:00', '10:30:00'),
    (table, 14.5, 20, '2024-04-20 10:30:00', '10:30:00'),
    (table, 15.5, 8, '2024-04-20 10:30:00', '10:30:00'),
    (table, 16.5, 5, '2024-04-20 10:30:00', '10:30:00'),
    (table, 17.5, 4, '2024-04-20 10:30:00', '10:30:00'),
    (table, 18.5, 10, '2024-04-20 10:30:00', '10:30:00'),
    (table, 15.2, 87.2, '2024-04-20 11:45:00', '11:45:00'),
    (table, 12.8, 25.3, '2024-04-20 13:20:00', '13:20:00')
]

# SQL query to check if data exists
check_query = "SELECT COUNT(*) FROM Cheer.{} WHERE DateTime = %s"

# SQL query to insert data
insert_query = """
INSERT INTO {} (Distance, Digital_Count, DateTime, Time) 
VALUES (%s, %s, %s, %s)
"""

# Executing the SQL query for each row of data
for row in data_to_insert:
    table_name = row[0]  # Extract table name from the tuple
    formatted_check_query = check_query.format(table_name)
    formatted_insert_query = insert_query.format(table_name)
    
    # Execute the check query
    cursor.execute(formatted_check_query, (row[3], ))
    result = cursor.fetchone()[0]  # Fetch the count
    print(result)
    if result == 0:  # If data doesn't exist, insert it
        pass
        #cursor.execute(formatted_insert_query, row[1:])

# Committing the changes
# connection.commit()

# Closing the cursor and connection
cursor.close()
connection.close()
