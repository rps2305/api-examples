# MySQL

## Overview
MySQL is a relational database. Applications connect over TCP (default 3306) using a driver. Query access can also be exposed through REST gateways.

## Python
```python
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="app_user",
    password="password",
    database="app_db",
)

cursor = conn.cursor()
cursor.execute("SELECT VERSION()")
print(cursor.fetchone())

cursor.close()
conn.close()
```

## PowerShell
```powershell
Add-Type -Path "C:\path\to\MySql.Data.dll"
$connectionString = "server=localhost;user=app_user;password=password;database=app_db"
$conn = New-Object MySql.Data.MySqlClient.MySqlConnection($connectionString)
$conn.Open()
$cmd = $conn.CreateCommand()
$cmd.CommandText = "SELECT VERSION()"
$reader = $cmd.ExecuteReader()
while ($reader.Read()) { $reader[0] }
$reader.Close()
$conn.Close()
```

## curl
```bash
# MySQL itself is not HTTP-based. Use an HTTP gateway like Adminer or a custom API.
```

## Docs
- https://dev.mysql.com/doc/
- https://dev.mysql.com/doc/connector-python/en/
