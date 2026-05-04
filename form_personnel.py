import sys
import sqlite3
from PyQt6.QtWidgets import (QApplication,QWidget,QVBoxLayout,QLineEdit,QComboBox,QPushButton,QLabel,QMessageBox)

#By placing (QWidget) after the class name, PersonnelForm inherits all properties,
#methods, and signals from QWidget. This means it can be displayed, painted on the screen, and handle user events.
#maong ayaw kalimot ani vhen.

class PersonnelForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DPWH Personnel Entry")
        self.setFixedWidth(400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Input Fields
        self.emp_id = QLineEdit(placeholderText="Employee ID (e.g., DVO-001)")
        self.last_name = QLineEdit(placeholderText="Last Name")
        self.first_name = QLineEdit(placeholderText="First Name")
        self.middle_name = QLineEdit(placeholderText="Middle Name")
        self.name_extension = QLineEdit(placeholderText="Extensions (Ex: Sr., Jr., II,)")
        self.division = QLineEdit(placeholderText="Division")
        self.position_title = QLineEdit(placeholderText= "Position Title")
        self.remarks = QLineEdit(placeholderText="Remarks")

        
        # Dropdown for Status (Enforces your CHECK constraint)
        self.status = QComboBox()
        self.status.addItems(["BUDGETARY", "COS"])

        # Save Button
        save_btn = QPushButton("Save to Database")
        save_btn.clicked.connect(self.save_data)

        # Adding to Layout
        layout.addWidget(QLabel("Employee ID:"))
        layout.addWidget(self.emp_id)
        layout.addWidget(QLabel("First Name:"))
        layout.addWidget(self.first_name)
        layout.addWidget(QLabel("Middle Name:"))
        layout.addWidget(self.middle_name)
        layout.addWidget(QLabel("Last Name:"))
        layout.addWidget(self.last_name)
        layout.addWidget(QLabel("Extensions (Ex: Sr., Jr., II.):"))
        layout.addWidget(self.name_extension)
        layout.addWidget(QLabel("Position:"))
        layout.addWidget(self.position_title)
        layout.addWidget(QLabel("Division:"))
        layout.addWidget(self.division)
        layout.addWidget(QLabel("Employment Status:"))
        layout.addWidget(self.status)
        layout.addWidget(QLabel("Remarks:"))
        layout.addWidget(self.remarks)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def save_data(self):
        # 1. Get data from the form
        e_id = self.emp_id.text()
        fn = self.first_name.text()
        mn = self.middle_name.text()
        ln = self.last_name.text()
        ext_n = self.name_extension.text()
        pos_title = self.position_title.text()
        div = self.division.text()
        st = self.status.currentText()
        rm = self.remarks.text()
   


        # 2. Database Logic
        try:
            db = sqlite3.connect('list_hrms.db')
            cursor = db.cursor()
            
            # Note: We must include 'division' etc. even if empty for now
            cursor.execute('''
                INSERT INTO personnel (emp_id, last_name, first_name, middle_name, name_extension, division, position_title, employment_status, remarks)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (e_id, ln, fn, mn, ext_n, div, pos_title, st, rm))
            
            db.commit()
            db.close()
            QMessageBox.information(self, "Success", "Personnel added successfully!")
            
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Duplicate Employee ID found!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed: {str(e)}")

# Standard PyQt6 execution
app = QApplication(sys.argv)
window = PersonnelForm()
window.show()
sys.exit(app.exec())