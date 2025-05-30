import os
import mysql.connector
from mysql.connector import Error

# Read DB config from environment variables (set in GitHub Actions secrets)
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME')
}

def execute_sql_script(file_path):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        with open(file_path, 'r') as f:
            sql_commands = f.read().split(';')

        for command in sql_commands:
            if command.strip():
                print(f"Executing:\n{command.strip()}\n")
                cursor.execute(command)

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
    execute_sql_script('projects.sql')
    execute_sql_script('add_departments.sql')
