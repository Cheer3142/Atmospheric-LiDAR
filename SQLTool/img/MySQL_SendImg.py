import mysql.connector

def upload_image(image_path):
    try:
        # Establishing connection to MySQL
        connection = mysql.connector.connect(
            host="192.168.2.190",
            port="1890",
            user="root",
            password="Cheer123",
            database="Cheer"
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Read the image file
            with open(image_path, "rb") as file:
                image_data = file.read()

            # Get image metadata
            filename = image_path.split("/")[-1]
            filetype = filename.split(".")[-1]
            filesize = len(image_data)

            # Insert image data into the database
            insert_query = "INSERT INTO Images (filename, filetype, filesize, image_data) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (filename, filetype, filesize, image_data))
            connection.commit()

            print("Image uploaded successfully.")

    except mysql.connector.Error as error:
        print("Failed to insert image into MySQL table:", error)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")

# Usage example:
upload_image("event1.jpg")
