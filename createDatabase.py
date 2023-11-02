import sqlite3

# Replace "my_database.db" with the desired database name
db_name = "banco.db"

# Create a connection to the database (this will create the database if it doesn't exist)
conn = sqlite3.connect(db_name)

# Close the connection
conn.close()
