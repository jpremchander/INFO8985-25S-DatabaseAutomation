import os
import datetime
import subprocess

# Database details
DB_HOST = 'localhost'
DB_USER = 'devdbuser'
DB_PASSWORD = 'devpwd123'  
DB_NAME = 'testdb'      
BACKUP_DIR = './dbbackups'

def create_backup():
    """Create a backup of the MySQL database"""
    
    # Create backup directory if it doesn't exist
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"Created directory: {BACKUP_DIR}")
    
    # Backup filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{DB_NAME}_backup_{timestamp}.sql"
    backup_path = os.path.join(BACKUP_DIR, backup_file)
    
    mysqldump_cmd = [
        'mysqldump',
        f'--host={DB_HOST}',
        f'--user={DB_USER}',
        f'--password={DB_PASSWORD}',
        '--single-transaction',  
        DB_NAME
    ]
    
    try:
        with open(backup_path, 'w') as f:
            process = subprocess.Popen(mysqldump_cmd, stdout=f, stderr=subprocess.PIPE)
            _, stderr = process.communicate()
        
        if process.returncode == 0:
            print(f"Backup created successfully: {backup_path}")
            return True
        else:
            print(f"Backup failed: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"Error creating backup: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting database backup...")
    create_backup()
    print("Backup process completed.")