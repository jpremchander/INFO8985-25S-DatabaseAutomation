import os
import re
import mysql.connector

# Database details
DB_HOST = 'localhost'
DB_USER = 'devdbuser'
DB_PASSWORD = 'devpwd123'
DB_NAME = 'testdb'  
CHANGES_DIR = './db_changes'    
VERSION_TABLE = 'db_changes_log' 

def connect_to_database():
    """Connect to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        print("Connected to database successfully")
        return connection
    except Exception as e:
        print(f"Failed to connect to database: {str(e)}")
        return None

def create_version_table(connection):
    """Create table to track database changes if it doesn't exist."""
    cursor = connection.cursor()
    
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {VERSION_TABLE} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        script_name VARCHAR(255) NOT NULL,
        applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    try:
        cursor.execute(create_table_sql)
        connection.commit()
        print(f"Version tracking table '{VERSION_TABLE}' is ready")
        return True
    except Exception as e:
        print(f"Error creating version table: {str(e)}")
        return False
    finally:
        cursor.close()

def get_deployed_scripts(connection):
    cursor = connection.cursor()
    deployed_scripts = []
    
    try:
        cursor.execute(f"SELECT script_name FROM {VERSION_TABLE}")
        for (script_name,) in cursor:
            deployed_scripts.append(script_name)
        return deployed_scripts
    except Exception as e:
        print(f"Error getting applied scripts: {str(e)}")
        return []
    finally:
        cursor.close()

def get_version_from_filename(filename):
    """Extract version number from filename"""
    match = re.match(r"V(\d+)_.*\.sql", filename, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return 999  

def get_pending_scripts(deployed_scripts):
    """Get list of SQL files that need to be deployed"""
    if not os.path.exists(CHANGES_DIR):
        os.makedirs(CHANGES_DIR)
        print(f"Created changes directory: {CHANGES_DIR}")
        return []
    
    # Pending deployment files
    pending_files = []
    for filename in os.listdir(CHANGES_DIR):
        if filename.endswith('.sql') and filename not in deployed_scripts:
            version = get_version_from_filename(filename)
            pending_files.append((version, filename))
    
    # Deployment Versions
    pending_files.sort()
    return [filename for _, filename in pending_files]

def apply_script(connection, script_name):
    """Execute a SQL script file."""
    script_path = os.path.join(CHANGES_DIR, script_name)
    cursor = connection.cursor()
    
    try:
        with open(script_path, 'r') as f:
            sql_content = f.read()
        
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        print(f"Applying {script_name} ({len(statements)} statements)...")
        
        for statement in statements:
            cursor.execute(statement)
        
        # Deployed version
        cursor.execute(
            f"INSERT INTO {VERSION_TABLE} (script_name) VALUES (%s)",
            (script_name,)
        )
        
        connection.commit()
        print(f"Successfully applied {script_name}")
        return True
        
    except Exception as e:
        connection.rollback()
        print(f"Error applying {script_name}: {str(e)}")
        return False
    finally:
        cursor.close()

def deploy_changes():
    """Main function to deploy database changes."""
    # Connect to database
    connection = connect_to_database()
    if not connection:
        return
    
    try:
        # Create deployment table if needed
        if not create_version_table(connection):
            return
        
        # Get list of scripts already deployed
        deployed_scripts = get_deployed_scripts(connection)
        print(f"Found {len(deployed_scripts)} previously applied scripts")
        
        # Get list of scripts that need to be deployed
        pending_scripts = get_pending_scripts(deployed_scripts)
        
        if not pending_scripts:
            print("No pending changes to apply")
            return
        
        print(f"Found {len(pending_scripts)} pending scripts to apply")
        
        success_count = 0
        for script_name in pending_scripts:
            if apply_script(connection, script_name):
                success_count += 1
        
        print(f"Deployment completed: {success_count}/{len(pending_scripts)} scripts applied")
        
    finally:
        connection.close()

if __name__ == "__main__":
    print("Starting database change deployment...")
    deploy_changes()
    print("Deployment process completed.")