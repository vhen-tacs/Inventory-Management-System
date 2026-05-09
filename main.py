import sys
import database
from form_personnel import PersonnelForm
from form_hardware import HardwareForm
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget, 
                             QFrame, QGridLayout, QGraphicsDropShadowEffect,
                             QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class LogsDialog(QDialog):
    """logs for Audit trail"""
    def __init__(self, module_name):
        super().__init__()
        self.setWindowTitle(f"Audit Trail: {module_name} Logs")
        self.resize(800, 400) # Made wider to fit the full details string
        self.setStyleSheet("background-color: white;")
        
        layout = QVBoxLayout(self)
        title = QLabel(f"{module_name} System Logs")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Timestamp", "Action", "Full Details"])
        
        # Viewer
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) 
        self.table.setWordWrap(True) # Force long text to wrap to the next line
        layout.addWidget(self.table)
        
        # Fetch and load logs
        logs = database.get_logs(module_name)
        self.table.setRowCount(len(logs))
        for row, log in enumerate(logs):
            for col, val in enumerate(log):
                self.table.setItem(row, col, QTableWidgetItem(str(val)))
                
        # Resize rows to fit the wrapped text
        self.table.resizeRowsToContents()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        database.init_db()

        self.setWindowTitle("DPWH ICT Inventory System")
        self.resize(1200, 750)

        self.setStyleSheet("""
            QMainWindow { background-color: #F3F4F6; }
            QLabel { font-family: 'Segoe UI', Arial, sans-serif; }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(240)
        self.sidebar.setStyleSheet("""
            QFrame { background-color: #1E293B; border-right: 1px solid #0F172A; }
            QPushButton { background-color: transparent; color: #94A3B8; text-align: left; padding: 12px 20px; font-size: 14px; font-family: 'Segoe UI', Arial; border: none; font-weight: 500; }
            QPushButton:hover { background-color: #334155; color: #FFFFFF; border-left: 4px solid #3B82F6; }
            QPushButton:checked { background-color: #0F172A; color: #3B82F6; border-left: 4px solid #3B82F6; font-weight: bold; }
        """)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(0, 20, 0, 20)
        self.sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.brand_label = QLabel("  DPWH ADMIN")
        self.brand_label.setStyleSheet("color: #FFFFFF; font-size: 20px; font-weight: bold; padding-left: 10px;")
        self.brand_sub = QLabel("    ICT Asset Management")
        self.brand_sub.setStyleSheet("color: #64748B; font-size: 12px; padding-left: 10px; margin-bottom: 20px;")
        self.sidebar_layout.addWidget(self.brand_label)
        self.sidebar_layout.addWidget(self.brand_sub)

        self.btn_dashboard = QPushButton(" 📊  Dashboard")
        self.btn_personnel = QPushButton(" 👥  Personnel")
        self.btn_hardware = QPushButton(" 💻  Hardware")
        
        for btn in [self.btn_dashboard, self.btn_personnel, self.btn_hardware]:
            btn.setCheckable(True)
            self.sidebar_layout.addWidget(btn)

        self.btn_dashboard.setChecked(True)

        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        self.header = QFrame()
        self.header.setFixedHeight(60)
        self.header.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E5E7EB;")
        self.header_layout = QHBoxLayout(self.header)
        self.header_layout.setContentsMargins(30, 0, 30, 0)
        
        self.page_title = QLabel("Dashboard Overview")
        self.page_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #111827; border: none;")
        self.user_info = QLabel("👤 Admin User | Davao City")
        self.user_info.setStyleSheet("font-size: 13px; color: #6B7280; border: none;")

        self.header_layout.addWidget(self.page_title)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.user_info)

        self.content_stack = QStackedWidget()
        self.setup_pages()

        self.content_layout.addWidget(self.header)
        self.content_layout.addWidget(self.content_stack)

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.content_area)

        self.btn_dashboard.clicked.connect(lambda: self.switch_page(0, self.btn_dashboard, "Dashboard Overview"))
        self.btn_personnel.clicked.connect(lambda: self.switch_page(1, self.btn_personnel, "Personnel Management"))
        self.btn_hardware.clicked.connect(lambda: self.switch_page(2, self.btn_hardware, "Hardware Inventory"))

        self.btn_add_staff.clicked.connect(self.add_personnel)
        self.btn_edit_staff.clicked.connect(self.edit_personnel)
        self.btn_del_staff.clicked.connect(self.delete_personnel)
        self.btn_logs_staff.clicked.connect(lambda: self.show_logs("Personnel"))

        self.btn_add_hw.clicked.connect(self.add_hardware)
        self.btn_edit_hw.clicked.connect(self.edit_hardware)
        self.btn_del_hw.clicked.connect(self.delete_hardware)
        self.btn_logs_hw.clicked.connect(lambda: self.show_logs("Hardware"))

    def setup_pages(self):
        self.page_dashboard = QWidget()
        dash_layout = QVBoxLayout(self.page_dashboard)
        dash_layout.setContentsMargins(30, 30, 30, 30)
        dash_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.refresh_dashboard()

        self.page_personnel = QWidget()
        personnel_layout = QVBoxLayout(self.page_personnel)
        
        btn_layout = QHBoxLayout()
        self.btn_add_staff = QPushButton("➕ Add")
        self.btn_edit_staff = QPushButton("✏️ Edit")
        self.btn_del_staff = QPushButton("🗑️ Remove")
        self.btn_logs_staff = QPushButton("📋 Show Logs")
        
        for btn in [self.btn_add_staff, self.btn_edit_staff, self.btn_del_staff, self.btn_logs_staff]:
            btn.setStyleSheet("padding: 8px 15px; background-color: #E2E8F0; border-radius: 4px; font-weight: bold;")
            btn_layout.addWidget(btn)
        btn_layout.addStretch() 
        
        self.personnel_table = QTableWidget()
        self.personnel_table.setColumnCount(10)
        self.personnel_table.setHorizontalHeaderLabels(["ID", "Emp ID", "First Name", "Middle Name", "Last Name", "Extension", "Division", "Position", "Status", "Remarks"])
        self.personnel_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.personnel_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.personnel_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        self.load_personnel_data()
        
        personnel_layout.addLayout(btn_layout)
        personnel_layout.addWidget(self.personnel_table)

        self.page_hardware = QWidget()
        hardware_layout = QVBoxLayout(self.page_hardware)
        hardware_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        hardware_layout.setContentsMargins(30, 30, 30, 30)

        btn_layout_hw = QHBoxLayout()
        self.btn_add_hw = QPushButton("➕ Add")
        self.btn_edit_hw = QPushButton("✏️ Edit")
        self.btn_del_hw = QPushButton("🗑️ Remove")
        self.btn_logs_hw = QPushButton("📋 Show Logs")
        
        for btn in [self.btn_add_hw, self.btn_edit_hw, self.btn_del_hw, self.btn_logs_hw]:
            btn.setStyleSheet("padding: 8px 15px; background-color: #E2E8F0; border-radius: 4px; font-weight: bold;")
            btn_layout_hw.addWidget(btn)
        btn_layout_hw.addStretch()

        self.hardware_table = QTableWidget()
        self.hardware_table.setColumnCount(10)
        self.hardware_table.setHorizontalHeaderLabels(["ID", "Type", "HW ID", "Serial", "Brand", "Model", "RAM", "Storage", "Status", "Division"])
        self.hardware_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.hardware_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.hardware_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        self.load_hardware_data()

        hardware_layout.addLayout(btn_layout_hw)
        hardware_layout.addWidget(self.hardware_table)

        self.content_stack.addWidget(self.page_dashboard)
        self.content_stack.addWidget(self.page_personnel)
        self.content_stack.addWidget(self.page_hardware)
        self.content_stack.setCurrentIndex(0)

    def refresh_dashboard(self):
        layout = self.page_dashboard.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget: widget.deleteLater()

        total_hw, total_staff, repair_count = database.get_dashboard_stats()
        grid_cards = QGridLayout()
        grid_cards.setSpacing(20)
        
        grid_cards.addWidget(self.create_stat_card("Total Hardware", str(total_hw), "#3B82F6"), 0, 0)
        grid_cards.addWidget(self.create_stat_card("Active Personnel", str(total_staff), "#10B981"), 0, 1)
        grid_cards.addWidget(self.create_stat_card("For Repair", str(repair_count), "#EF4444"), 0, 2)
        layout.addLayout(grid_cards)

    def create_stat_card(self, title, value, color_hex):
        card = QFrame()
        card.setFixedHeight(120)
        card.setStyleSheet(f"QFrame {{ background-color: white; border-radius: 8px; border-top: 4px solid {color_hex}; }}")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 20))
        shadow.setOffset(0, 4)
        card.setGraphicsEffect(shadow)

        layout = QVBoxLayout(card)
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #6B7280; font-size: 14px; font-weight: bold;")
        lbl_value = QLabel(value)
        lbl_value.setStyleSheet("color: #111827; font-size: 32px; font-weight: bold;")
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_value)
        layout.addStretch()
        return card

    def switch_page(self, index, button, title):
        self.btn_dashboard.setChecked(False)
        self.btn_personnel.setChecked(False)
        self.btn_hardware.setChecked(False)
        button.setChecked(True)
        self.content_stack.setCurrentIndex(index)
        self.page_title.setText(title)
        
        if index == 0: self.refresh_dashboard()
        elif index == 1: self.load_personnel_data()
        elif index == 2: self.load_hardware_data()

    def load_personnel_data(self):
        data = database.get_all_personnel()
        self.personnel_table.setRowCount(len(data))
        for row, record in enumerate(data):
            for col, value in enumerate(record):
                self.personnel_table.setItem(row, col, QTableWidgetItem(str(value)))

    def load_hardware_data(self):
        data = database.get_all_hardware()
        self.hardware_table.setRowCount(len(data))
        for row, record in enumerate(data):
            selected_cols = [0, 1, 2, 3, 4, 5, 7, 8, 12, 13] 
            for col_idx, data_idx in enumerate(selected_cols):
                self.hardware_table.setItem(row, col_idx, QTableWidgetItem(str(record[data_idx])))

    def add_personnel(self):
        self.personnel_form = PersonnelForm()
        self.personnel_form.show()

    def edit_personnel(self):
        selected_rows = self.personnel_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a personnel record to edit.")
            return
        row = selected_rows[0].row()
        data = [self.personnel_table.item(row, col).text() if self.personnel_table.item(row, col) else "" for col in range(self.personnel_table.columnCount())]
        self.personnel_form = PersonnelForm(data)
        self.personnel_form.show()

    def delete_personnel(self):
        selected_rows = self.personnel_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a personnel record to delete.")
            return
        row = selected_rows[0].row()
        record_id = self.personnel_table.item(row, 0).text() 
        emp_id = self.personnel_table.item(row, 1).text() 
        
        reply = QMessageBox.question(self, "Confirm Remove", f"Remove employee {emp_id}?\n\nThis will hide them from the app and record the action in the logs.", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            database.delete_personnel(record_id, emp_id)
            self.load_personnel_data()
            self.refresh_dashboard()

    def add_hardware(self):
        self.hardware_form = HardwareForm()
        self.hardware_form.show()

    def edit_hardware(self):
        selected_rows = self.hardware_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a hardware record to edit.")
            return
        row = selected_rows[0].row()
        hw_id = self.hardware_table.item(row, 0).text() 
        data = database.get_all_hardware()
        for record in data:
            if str(record[0]) == hw_id:
                self.hardware_form = HardwareForm(record)
                self.hardware_form.show()
                break

    def delete_hardware(self):
        selected_rows = self.hardware_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a hardware record to delete.")
            return
        row = selected_rows[0].row()
        record_id = self.hardware_table.item(row, 0).text()
        hw_name = self.hardware_table.item(row, 2).text()
        
        reply = QMessageBox.question(self, "Confirm Remove", f"Remove hardware {hw_name}?\n\nThis will hide the equipment from the app and record the action in the logs.", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            database.delete_hardware(record_id, hw_name)
            self.load_hardware_data()
            self.refresh_dashboard()

    def show_logs(self, module_name):
        self.log_window = LogsDialog(module_name)
        self.log_window.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
