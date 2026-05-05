import sqlite3

def create_hardware_list():
    #connect
    db = sqlite3.connect('list_hrms.db')
    cursor = db.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hardware_list(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hardware_type TEXT NOT NULL CHECK (hardware_type IN ('Desktop','Laptop','Printer')),
            hw_id TEXT UNIQUE NOT NULL,
            serial_number TEXT UNIQUE NOT NULL,
            brand_name TEXT NOT NULL,
            model_name TEXT NOT NULL,
            processor_details TEXT NOT NULL,
            ram TEXT NOT NULL,
            storage TEXT NOT NULL,
            os_ver TEXT NOT NULL,
            ms_office_ver TEXT NOT NULL,
            anti_virus TEXT NOT NULL,
            hardware_status TEXT NOT NULL CHECK (hardware_status IN ('Serviceable','For Repair', 'Unserviceable','Operational')),
            division TEXT NULL,
            property_no TEXT NOT NULL,
            year_acquired TEXT NOT NULL,
            user_id TEXT,
            par_id TEXT,
            FOREIGN KEY (user_id) REFERENCES personnel (emp_id),
            FOREIGN KEY (par_id) REFERENCES personnel (emp_id)
                
                )
                ''')

    db.commit()
    db.close()
    print("Hardware table successfully added to list_hrms.db!")

if __name__ == "__main__":
    create_hardware_list()