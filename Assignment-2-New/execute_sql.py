def execute_sql_script(script_path):
    connection = None  # define outside try block
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='devdbuser',
            password='devpwd123',
            database='companydb'
        )

        if connection.is_connected():
            print("Connected to the database.")
            cursor = connection.cursor()

            with open(script_path, 'r') as file:
                sql_script = file.read()

            for statement in sql_script.split(';'):
                stmt = statement.strip()
                if stmt:
                    cursor.execute(stmt)
            connection.commit()
            print("SQL script executed successfully.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection and connection.is_connected():
            connection.close()
            print("Connection closed.")
