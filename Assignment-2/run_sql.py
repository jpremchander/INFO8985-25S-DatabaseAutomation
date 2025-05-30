# run_sql.py
# This script connects to a MySQL database and executes an SQL script file.
import mysql.connector
from mysql.connector import Error
import os

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME')
}

def execute_sql_script(file_path):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        with open(file_path, 'r') as f:
            sql_commands = f.read().split(';')

        for command in sql_commands:
            if command.strip():
                cursor.execute(command)
                print(f"Executed:\n{command.strip()}\n")

        conn.commit()
        print("SQL script executed and committed successfully.")

    except Error as e:
        print("Error:", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    execute_sql_script('add_departments.sql')
