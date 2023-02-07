import sqlite3

con = sqlite3.connect("taskdb.db")
cur = con.cursor()
cur.execute("""
SELECT * FROM tasks
""")
print(cur.fetchall())
