import mysql.connector
from mysql.connector import Error

def execute_sql_script(script_path):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='devdbuser',
            password='devpwd123',
            database='companydb'
        )
        cursor = connection.cursor()

        with open(script_path, 'r') as file:
            sql_commands = file.read().split(';')

        for command in sql_commands:
            command = command.strip()
            if command:
                cursor.execute(command)

        connection.commit()
        print("SQL script executed successfully.")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    execute_sql_script('schema_changes.sql')
