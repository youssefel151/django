# PCRM Django Project

## Run the server manually on Windows

Open PowerShell or Command Prompt in this folder:

```powershell
cd "C:\Users\PC\Desktop\youssef_elghoul - Copy\CRMPROJECT\pcrm"
.\start_server.bat
```

Then open:

```text
http://127.0.0.1:8000/
```

By default this uses a local SQLite database file named `db.sqlite3`, which is the easiest setup for manual development.

## User roles

The project includes Django authentication for a school management system:

- Admin
- Enseignant
- Etudiant

New users can select a role during registration. After login, each user is redirected to the matching dashboard.

To create a Django super-admin account for `/admin/`, run:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

## Use MySQL instead

If you want to use the original MySQL database, make sure MySQL is running and the `db_crm` database exists, then start Django with:

```powershell
$env:USE_MYSQL="1"
.\start_server.bat
```

You can also override these optional values:

```powershell
$env:MYSQL_DATABASE="db_crm"
$env:MYSQL_USER="root"
$env:MYSQL_PASSWORD="123"
$env:MYSQL_HOST="localhost"
$env:MYSQL_PORT="3306"
```
