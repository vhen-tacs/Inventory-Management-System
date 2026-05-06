import sys
import sqlite3
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QLabel, QMessageBox)

class PersonnelForm(QWidget):
    def __init__(self, personnel_data=None):
        super().__init__()
        self.personnel_data = personnel_data 
        self.setWindowTitle("DPWH Personnel Entry" if not personnel_data else "Edit Personnel")
        self.setFixedWidth(400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.emp_id = QLineEdit(placeholderText="Employee ID (e.g., DVO-001)")
        self.last_name = QLineEdit(placeholderText="Last Name")
        self.first_name = QLineEdit(placeholderText="First Name")
        self.middle_name = QLineEdit(placeholderText="Middle Name")
        self.name_extension = QLineEdit(placeholderText="Extensions (Ex: Sr., Jr., II,)")
        self.division = QLineEdit(placeholderText="Division")
        self.position_title = QLineEdit(placeholderText= "Position Title")
        self.remarks = QLineEdit(placeholderText="Remarks")
        
        self.status = QComboBox()
        self.status.addItems(["BUDGETARY", "COS"])

        if self.personnel_data:
            self.emp_id.setText(self.personnel_data[1])
            self.first_name.setText(self.personnel_data[2])
            self.middle_name.setText(self.personnel_data[3])
            self.last_name.setText(self.personnel_data[4])
            self.name_extension.setText(self.personnel_data[5])
            self.division.setText(self.personnel_data[6])
            self.position_title.setText(self.personnel_data[7])
            self.status.setCurrentText(self.personnel_data[8])
            self.remarks.setText(self.personnel_data[9])

        save_btn = QPushButton("Save to Database" if not self.personnel_data else "Update Record")
        save_btn.clicked.connect(self.save_data)

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
        e_id = self.emp_id.text()
        fn = self.first_name.text()
        mn = self.middle_name.text()
        ln = self.last_name.text()
        ext_n = self.name_extension.text()
        pos_title = self.position_title.text()
        div = self.division.text()
        st = self.status.currentText()
        rm = self.remarks.text()
   
        try:
            db = sqlite3.connect('list_hrms.db')
            cursor = db.cursor()
            
            if self.personnel_data:
                cursor.execute('''
                    UPDATE personnel SET emp_id=?, last_name=?, first_name=?, middle_name=?, name_extension=?, division=?, position_title=?, employment_status=?, remarks=? WHERE id=?
                ''', (e_id, ln, fn, mn, ext_n, div, pos_title, st, rm, self.personnel_data[0]))
                QMessageBox.information(self, "Success", "Personnel updated successfully!")
            else:
                cursor.execute('''
                    INSERT INTO personnel (emp_id, last_name, first_name, middle_name, name_extension, division, position_title, employment_status, remarks)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (e_id, ln, fn, mn, ext_n, div, pos_title, st, rm))
                QMessageBox.information(self, "Success", "Personnel added successfully!")
            
            db.commit()
            db.close()
            
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Duplicate Employee ID found!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed: {str(e)}")

        finally:
            # THIS GUARANTEES THE DATABASE UNLOCKS
            if db:
                db.close()

if __name__ == "__main__":
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    window = PersonnelForm()
    window.show()
    sys.exit(app.exec())