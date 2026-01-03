# Microsoft SQL Server

## Overview
Microsoft SQL Server is a relational database accessible via TDS over TCP (default 1433). Use drivers like `pyodbc` or `SqlClient` for access.

## Python
```python
import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=app_db;UID=app_user;PWD=password;Encrypt=yes;TrustServerCertificate=yes"
)

cursor = conn.cursor()
cursor.execute("SELECT @@VERSION")
print(cursor.fetchone())

cursor.close()
conn.close()
```

## PowerShell
```powershell
$connectionString = "Server=localhost;Database=app_db;User Id=app_user;Password=password;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connectionString)
$conn.Open()
$cmd = $conn.CreateCommand()
$cmd.CommandText = "SELECT @@VERSION"
$reader = $cmd.ExecuteReader()
while ($reader.Read()) { $reader[0] }
$reader.Close()
$conn.Close()
```

## curl
```bash
# SQL Server is not HTTP-based. Use drivers or a REST gateway if needed.
```

## Docs
- https://learn.microsoft.com/sql/sql-server/
- https://learn.microsoft.com/sql/connect/python/python-driver-for-sql-server
