import sys
import sqlite3
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QLabel, QMessageBox, QGridLayout)

class HardwareForm(QWidget):
    def __init__(self, hardware_data=None):
        super().__init__()
        self.hardware_data = hardware_data  # For editing
        self.setWindowTitle("DPWH Hardware Entry" if not hardware_data else "Edit Hardware")
        self.setFixedWidth(500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Input Fields
        self.hardware_type = QComboBox()
        self.hardware_type.addItems(["Desktop", "Laptop", "Printer"])

        self.hw_id = QLineEdit(placeholderText="Hardware ID (e.g., HW-001)")
        self.serial_number = QLineEdit(placeholderText="Serial Number")
        self.brand_name = QLineEdit(placeholderText="Brand Name")
        self.model_name = QLineEdit(placeholderText="Model Name")
        self.processor_details = QLineEdit(placeholderText="Processor Details")
        self.ram = QLineEdit(placeholderText="RAM (e.g., 8GB)")
        self.storage = QLineEdit(placeholderText="Storage (e.g., 512GB SSD)")
        self.os_ver = QLineEdit(placeholderText="OS Version")
        self.ms_office_ver = QLineEdit(placeholderText="MS Office Version")
        self.anti_virus = QLineEdit(placeholderText="Anti-Virus")
        self.hardware_status = QComboBox()
        self.hardware_status.addItems(["Serviceable", "For Repair", "Unserviceable", "Operational"])
        self.division = QLineEdit(placeholderText="Division")
        self.property_no = QLineEdit(placeholderText="Property Number")
        self.year_acquired = QLineEdit(placeholderText="Year Acquired")
        self.user_id = QLineEdit(placeholderText="User ID (Employee ID)")
        self.par_id = QLineEdit(placeholderText="PAR ID (Employee ID)")

        # Pre-fill if editing
        if self.hardware_data:
            self.hardware_type.setCurrentText(self.hardware_data[1])  # hardware_type
            self.hw_id.setText(self.hardware_data[2])  # hw_id
            self.serial_number.setText(self.hardware_data[3])  # serial_number
            self.brand_name.setText(self.hardware_data[4])  # brand_name
            self.model_name.setText(self.hardware_data[5])  # model_name
            self.processor_details.setText(self.hardware_data[6])  # processor_details
            self.ram.setText(self.hardware_data[7])  # ram
            self.storage.setText(self.hardware_data[8])  # storage
            self.os_ver.setText(self.hardware_data[9])  # os_ver
            self.ms_office_ver.setText(self.hardware_data[10])  # ms_office_ver
            self.anti_virus.setText(self.hardware_data[11])  # anti_virus
            self.hardware_status.setCurrentText(self.hardware_data[12])  # hardware_status
            self.division.setText(self.hardware_data[13])  # division
            self.property_no.setText(self.hardware_data[14])  # property_no
            self.year_acquired.setText(self.hardware_data[15])  # year_acquired
            self.user_id.setText(self.hardware_data[16])  # user_id
            self.par_id.setText(self.hardware_data[17])  # par_id

        # Save Button
        save_btn = QPushButton("Save to Database" if not self.hardware_data else "Update Record")
        save_btn.clicked.connect(self.save_data)
        layout= QGridLayout()
        # Adding to Layout
        layout.addWidget(QLabel("Hardware Type:"), 0,0)
        layout.addWidget(self.hardware_type, 0,1)
        layout.addWidget(QLabel("Hardware ID:"), 1,0)
        layout.addWidget(self.hw_id, 1,1)
        layout.addWidget(QLabel("Serial Number:"), 2,0)
        layout.addWidget(self.serial_number)
        layout.addWidget(QLabel("Brand Name:"), 3,0)
        layout.addWidget(self.brand_name)
        layout.addWidget(QLabel("Model Name:"), 4,0)
        layout.addWidget(self.model_name)
        layout.addWidget(QLabel("Processor Details:"), 5,0)
        layout.addWidget(self.processor_details)
        layout.addWidget(QLabel("RAM:"), 6,0)
        layout.addWidget(self.ram)
        layout.addWidget(QLabel("Storage:"), 7,0)
        layout.addWidget(self.storage)
        layout.addWidget(QLabel("OS Version:"))
        layout.addWidget(self.os_ver)
        layout.addWidget(QLabel("MS Office Version:"))
        layout.addWidget(self.ms_office_ver)
        layout.addWidget(QLabel("Anti-Virus:"))
        layout.addWidget(self.anti_virus)
        layout.addWidget(QLabel("Hardware Status:"))
        layout.addWidget(self.hardware_status)
        layout.addWidget(QLabel("Division:"))
        layout.addWidget(self.division)
        layout.addWidget(QLabel("Property Number:"))
        layout.addWidget(self.property_no)
        layout.addWidget(QLabel("Year Acquired:"))
        layout.addWidget(self.year_acquired)
        layout.addWidget(QLabel("User ID:"))
        layout.addWidget(self.user_id)
        layout.addWidget(QLabel("PAR ID:"))
        layout.addWidget(self.par_id)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def save_data(self):
        # Get data from the form
        hw_type = self.hardware_type.currentText()
        hw_id_val = self.hw_id.text()
        serial = self.serial_number.text()
        brand = self.brand_name.text()
        model = self.model_name.text()
        processor = self.processor_details.text()
        ram = self.ram.text()
        storage = self.storage.text()
        os_ver = self.os_ver.text()
        ms_office = self.ms_office_ver.text()
        av = self.anti_virus.text()
        status = self.hardware_status.currentText()
        division = self.division.text()
        prop_no = self.property_no.text()
        year = self.year_acquired.text()
        user_id = self.user_id.text()
        par_id = self.par_id.text()

        # Database Logic
        try:
            db = sqlite3.connect('list_hrms.db')
            cursor = db.cursor()

            if self.hardware_data:
                # Update existing record
                cursor.execute('''
                    UPDATE hardware_list SET hardware_type=?, hw_id=?, serial_number=?, brand_name=?, model_name=?, processor_details=?, ram=?, storage=?, os_ver=?, ms_office_ver=?, anti_virus=?, hardware_status=?, division=?, property_no=?, year_acquired=?, user_id=?, par_id=? WHERE id=?
                ''', (hw_type, hw_id_val, serial, brand, model, processor, ram, storage, os_ver, ms_office, av, status, division, prop_no, year, user_id, par_id, self.hardware_data[0]))
                QMessageBox.information(self, "Success", "Hardware updated successfully!")
            else:
                # Insert new record
                cursor.execute('''
                    INSERT INTO hardware_list (hardware_type, hw_id, serial_number, brand_name, model_name, processor_details, ram, storage, os_ver, ms_office_ver, anti_virus, hardware_status, division, property_no, year_acquired, user_id, par_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (hw_type, hw_id_val, serial, brand, model, processor, ram, storage, os_ver, ms_office, av, status, division, prop_no, year, user_id, par_id))
                QMessageBox.information(self, "Success", "Hardware added successfully!")

            db.commit()
            db.close()

        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Duplicate Hardware ID or Serial Number found!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed: {str(e)}")
