import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "your_user",
    "password": "your_password",
    "database": "companydb"
}

def apply_sql_script(file_path):
    with open(file_path, "r") as f:
        sql_commands = f.read().split(";")

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        for cmd in sql_commands:
            cmd = cmd.strip()
            if cmd:
                cursor.execute(cmd)
        conn.commit()
        print("✅ Schema changes applied successfully.")
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    apply_sql_script("schema_changes.sql")