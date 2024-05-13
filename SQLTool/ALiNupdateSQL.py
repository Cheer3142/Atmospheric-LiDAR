import mysql.connector

def Connect():
    connection = mysql.connector.connect(
        host="192.168.2.190",
        port="1890",
        user="root",
        password="Cheer123",
        database="Cheer"
    )

    # Creating a cursor object
    return connection, connection.cursor() # connection and cursor
    
def InsertMany(table_name, data_list, cursor):
    insert_query = """
    INSERT INTO {} (Distance, Digital_Count, DateTime, Time) 
    VALUES (%s, %s, %s, %s)
    """.format(table_name)
    
    cursor.executemany(insert_query, data_list)
        
def Commit(connection, cursor):
    # Committing the changes
    connection.commit()
    
    # Closing the cursor and connection
    cursor.close()
    connection.close()

if __name__ == '__main__':
    table = 'ALiN'
    # Sample data to insert
    data_to_insert = [
        (12.5, 2, '2024-04-20 10:30:00', '10:30:00'),
        (13.5, 7, '2024-04-20 10:30:00', '10:30:00'),
        (14.5, 20, '2024-04-20 10:30:00', '10:30:00'),
        (15.5, 8, '2024-04-20 10:30:00', '10:30:00'),
        (16.5, 5, '2024-04-20 10:30:00', '10:30:00'),
        (17.5, 4, '2024-04-20 10:30:00', '10:30:00'),
        (18.5, 10, '2024-04-20 10:30:00', '10:30:00'),
        (15.2, 87.2, '2024-04-20 11:45:00', '11:45:00'),
        (12.8, 25.3, '2024-04-20 13:20:00', '13:20:00')
    ]

    con, cur = Connect()
    # Inserting multiple rows in a single statement
    InsertMany(table, data_to_insert, cur)
    Commit(con, cur)
