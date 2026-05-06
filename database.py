import sqlite3

DB_FILE = 'list_hrms.db'

def init_db():
    """Safely upgrades the database to support Soft Deletes and Logging."""
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            module TEXT,
            action TEXT,
            details TEXT
        )
    ''')
    
    try:
        cursor.execute("ALTER TABLE personnel ADD COLUMN is_active INTEGER DEFAULT 1")
    except sqlite3.OperationalError:
        pass 
        
    try:
        cursor.execute("ALTER TABLE hardware_list ADD COLUMN is_active INTEGER DEFAULT 1")
    except sqlite3.OperationalError:
        pass 

    db.commit()
    db.close()

def log_action(module, action, details):
    """Saves an action to the system logs."""
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    cursor.execute("INSERT INTO system_logs (module, action, details) VALUES (?, ?, ?)", (module, action, details))
    db.commit()
    db.close()

def get_logs(module):
    """Fetches logs for a specific module."""
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    cursor.execute("SELECT timestamp, action, details FROM system_logs WHERE module = ? ORDER BY id DESC", (module,))
    data = cursor.fetchall()
    db.close()
    return data

def get_dashboard_stats():
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM hardware_list WHERE is_active = 1 OR is_active IS NULL")
        total_hw = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM personnel WHERE is_active = 1 OR is_active IS NULL")
        total_personnel = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM hardware_list WHERE hardware_status = 'For Repair' AND (is_active = 1 OR is_active IS NULL)")
        repair_count = cursor.fetchone()[0]
        return total_hw, total_personnel, repair_count
    except sqlite3.OperationalError:
        return 0, 0, 0
    finally:
        db.close()

def get_all_personnel():
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    cursor.execute("SELECT id, emp_id, first_name, middle_name, last_name, name_extension, division, position_title, employment_status, remarks FROM personnel WHERE is_active = 1 OR is_active IS NULL")
    data = cursor.fetchall()
    db.close()
    return data

def get_all_hardware():
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    cursor.execute("SELECT id, hardware_type, hw_id, serial_number, brand_name, model_name, processor_details, ram, storage, os_ver, ms_office_ver, anti_virus, hardware_status, division, property_no, year_acquired, user_id, par_id FROM hardware_list WHERE is_active = 1 OR is_active IS NULL")
    data = cursor.fetchall()
    db.close()
    return data

def delete_personnel(record_id, reference_name=""):
    """Fetches ALL details, performs the Soft Delete, and logs the full data."""
    db = sqlite3.connect(DB_FILE)
    db.row_factory = sqlite3.Row # This allows us to grab the column names
    cursor = db.cursor()
    
    # 1. Fetch the entire record BEFORE we hide it
    cursor.execute("SELECT * FROM personnel WHERE id=?", (record_id,))
    row = cursor.fetchone()
    
    if row:
        # Loop through every column, ignore blanks, and format it cleanly
        details_list = [f"{k.replace('_', ' ').title()}: {row[k]}" for k in row.keys() if k not in ('id', 'is_active') and row[k]]
        full_details_str = " | ".join(details_list)
    else:
        full_details_str = f"Removed Employee ID: {reference_name}"

    # 2. Hide the record
    cursor.execute("UPDATE personnel SET is_active = 0 WHERE id=?", (record_id,))
    db.commit()
    db.close()
    
    # 3. Log the full string
    log_action("Personnel", "Deleted", full_details_str)

def delete_hardware(record_id, reference_name=""):
    """Fetches ALL details, performs the Soft Delete, and logs the full data."""
    db = sqlite3.connect(DB_FILE)
    db.row_factory = sqlite3.Row 
    cursor = db.cursor()
    
    # 1. Fetch the entire record BEFORE we hide it
    cursor.execute("SELECT * FROM hardware_list WHERE id=?", (record_id,))
    row = cursor.fetchone()
    
    if row:
        # Loop through every column, ignore blanks, and format it cleanly
        details_list = [f"{k.replace('_', ' ').title()}: {row[k]}" for k in row.keys() if k not in ('id', 'is_active') and row[k]]
        full_details_str = " | ".join(details_list)
    else:
        full_details_str = f"Removed Hardware: {reference_name}"

    # 2. Hide the record
    cursor.execute("UPDATE hardware_list SET is_active = 0 WHERE id=?", (record_id,))
    db.commit()
    db.close()
    
    # 3. Log the full string
    log_action("Hardware", "Deleted", full_details_str)