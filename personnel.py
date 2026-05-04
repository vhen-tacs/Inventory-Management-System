import sqlite3

#connect
db = sqlite3.connect('list_hrms.db')
cursor = db.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS personnel(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id TEXT UNIQUE NOT NULL,
        last_name TEXT NOT NULL,
        first_name TEXT NOT NULL,
        middle_name TEXT,
        name_extension TEXT,
        division TEXT NOT NULL,
        position_title TEXT NOT NULL,
        employment_status TEXT NOT NULL CHECK (employment_status IN ('BUDGETARY','COS')),
        remarks TEXT   
               )            
               ''')
db.commit()
db.close()
print("Personnel Database created successfully!")
