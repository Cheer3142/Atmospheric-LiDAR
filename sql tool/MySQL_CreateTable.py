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

# SQL query to create a table
create_table_query = """
CREATE TABLE IF NOT EXISTS Weather (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Temp FLOAT,
    Windspeed FLOAT,
    Humid FLOAT,
    Dewpoint FLOAT,
    AirPressure FLOAT,
    DateTime DATETIME
)
"""

'''
create_table_query = """
CREATE TABLE IF NOT EXISTS ALiN (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Digital_Count FLOAT,
    Distance FLOAT,
    DateTime DATETIME,
    Time TIME
)
"""

create_table_query = """
CREATE TABLE Images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    filetype VARCHAR(100) NOT NULL,
    filesize INT NOT NULL,
    image_data LONGBLOB NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
'''

# Executing the SQL query
cursor.execute(create_table_query)

# Committing the changes
connection.commit()

# Closing the cursor and connection
cursor.close()
connection.close()
