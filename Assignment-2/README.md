# Assignment 2 - Database Schema Automation with GitHub Actions

**Course**: INFO8985-25S - Database Automation  
**StudentName**: Premchander Jebastian  

---

## 📌 Objective

Automate MySQL database schema changes using Python and GitHub Actions CI/CD pipeline. This assignment connects to an AWS RDS MySQL instance and applies schema changes using `.sql` scripts stored in the repository.

---

## 🗂️ Project Structure

Assignment-2/
├── add_departments.sql # SQL script to add departments table
├── projects.sql # SQL script to create projects table and add column
├── run_sql.py # Python script to execute SQL files on RDS
├── README.md # Assignment documentation
└── .github/
└── workflows/
└── run-schema.yml # GitHub Actions workflow file

yaml
Copy
Edit

---

## ⚙️ Setup Instructions

### 1. **Create AWS RDS MySQL Instance**
- Region: `us-east-1`
- DB Name: `companydb`
- Username: `cdbadmin`
- Password: `cdbpasswd`
- Security Group: Allow inbound MySQL (port 3306) from GitHub Actions (optional: `0.0.0.0/0` for testing)

---

### 2. **Configure GitHub Repository Secrets**

Go to your repository > Settings > Secrets and Variables > Actions > Add the following:

| Secret Name | Value                          |
|-------------|--------------------------------|
| `DB_HOST`   | `<your-rds-endpoint>` (e.g., `companydb.c2hmic0i8ifz.us-east-1.rds.amazonaws.com`) |
| `DB_USER`   | `cdbadmin`                     |
| `DB_PASS`   | `cdbpasswd`                    |
| `DB_NAME`   | `companydb`                    |

---

### 3. **Python Script: `run_sql.py`**

- Connects to the RDS instance using the secrets.
- Executes the SQL files (`projects.sql`, `add_departments.sql`) sequentially.
- Commits all changes.

---

### 4. **CI/CD Workflow: GitHub Actions**

The `.github/workflows/run-schema.yml` file triggers the automation on every push to the `main` branch.

#### Example Workflow Summary:
```yaml
- Checkout code
- Set up Python
- Install dependencies (`mysql-connector-python`)
- Run Python script with SQL commands
✅ Output
When the pipeline runs:

Creates projects and departments tables (if they don't exist).

Adds budget column to projects table.

Handles duplicate column errors gracefully and continues execution.

📷 Screenshots
(You can paste here screenshots from the GitHub Actions run or SQL query results from RDS)

💡 Notes
The Python script gracefully skips errors like Duplicate column name.

Use parameterized secrets for secure credential management.

Ensure the RDS instance is publicly accessible for GitHub Actions.

📚 References
MySQL Connector Python Docs

GitHub Actions Documentation

AWS RDS MySQL

🧑‍💻 Author
Student Name: Prem Chander Jebastian
Student ID: 9015480
Cloud Development & Operations - Spring'25
Conestoga College