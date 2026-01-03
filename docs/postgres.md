# PostgreSQL

## Overview
PostgreSQL is a relational database. Connect using the native protocol on port 5432 or via a REST gateway if needed.

## Python
```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="app_db",
    user="app_user",
    password="password",
)

with conn.cursor() as cursor:
    cursor.execute("SELECT version()")
    print(cursor.fetchone())

conn.close()
```

## PowerShell
```powershell
Add-Type -Path "C:\path\to\Npgsql.dll"
$connectionString = "Host=localhost;Username=app_user;Password=password;Database=app_db"
$conn = New-Object Npgsql.NpgsqlConnection($connectionString)
$conn.Open()
$cmd = $conn.CreateCommand()
$cmd.CommandText = "SELECT version()"
$reader = $cmd.ExecuteReader()
while ($reader.Read()) { $reader[0] }
$reader.Close()
$conn.Close()
```

## curl
```bash
# PostgreSQL is not HTTP-based. Use a REST gateway like PostgREST if needed.
```

## Docs
- https://www.postgresql.org/docs/
- https://www.psycopg.org/
