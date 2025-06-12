### PROG8850 - Assignment 2  
**Automating Database Schema Changes and Implementing CI/CD for Database Deployment**  


---

## 🔹 Project Overview

This project demonstrates how to:
- Automate database schema changes using Python and SQL scripts.
- Implement a CI/CD pipeline using GitHub Actions.
- Optionally deploy to Azure MySQL for real-world production scenarios.
- Run and test the setup both locally (via Ansible) and in GitHub Codespaces.

---

## 🔹 Project Structure

Assignment-2-New/
├── create_projects.sql
├── execute_sql.py
├── add_departments.sql
├── run_add_departments.py
├── requirements.txt
├── up.yml # Ansible playbook to start MySQL
├── down.yml # Ansible playbook to stop MySQL
└── .github/
└── workflows/
└── dc-cicd.yml # GitHub Actions workflow

---

## 🔹 Question 1: Automating Database Schema Changes

Files:
- `create_projects.sql`: Creates the `projects` table.

- `execute_sql.py`: Executes the SQL script and adds a `budget` column.

### ✅ How to Run Locally

1. **Install Python dependencies**

pip install -r requirements.txt

Start MySQL using Ansible

ansible-playbook up.yml

Run the schema change

python execute_sql.py

Access MySQL manually


mysql -u root -h 127.0.0.1 -p
---

## 🔹  Question 2: CI/CD Pipeline with GitHub Actions

Files:

.github/workflows/dc-cicd.yml: GitHub Actions workflow triggered on push to test.

add_departments.sql: Adds departments table.

run_add_departments.py: Executes schema change from workflow.

✅ GitHub Actions Highlights
Uses MySQL 5.7 Docker container with health checks.

Executes Python-based schema updates.

Supports both local and Azure MySQL configurations via secrets or defaults.

🔹 Azure MySQL Configuration (Optional)
You can use a real Azure Database for MySQL as your target:

✅ Azure Setup Checklist:
Server: Azure Database for MySQL Flexible Server

Database Name: companydb

Public Access: Enabled

Allow Azure Services: Enabled

Username: e.g., youradmin@yourserver

Password: strong password

✅ Set the following GitHub Secrets:

Secret Name	Example Value

DB_HOST	yourserver.mysql.database.azure.com
DB_USER	youradmin@yourserver
DB_PASSWORD	your-strong-password
DB_NAME	companydb

GitHub Actions will automatically use these credentials if present.

🔹 Local CI/CD Simulation via act
You can simulate GitHub Actions locally:


bin/act
# or
bin/act -P ubuntu-latest=-self-hosted
🔹 Codespaces Instructions
Open Codespace from GitHub

Install Ansible:


sudo apt update && sudo apt install -y ansible
Start MySQL:


ansible-playbook up.yml
Run script:


python execute_sql.py
Shut down:


ansible-playbook down.yml

✅ GitHub Actions Status

Feature	Status

Trigger on push to main branch - Push
MySQL 5.7 service setup
Execute schema change
Azure integration supported
Logs and debug info 