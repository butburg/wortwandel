#!/usr/bin/env python3
import sqlite3
import sys

if len(sys.argv) < 3:
    print("Usage: python run_sqlite_query.py <db_path> <query>")
    sys.exit(1)

db_path = sys.argv[1]
query = sys.argv[2]

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(row)
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()
