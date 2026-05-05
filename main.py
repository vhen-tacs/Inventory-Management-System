import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget, 
                             QFrame, QGridLayout, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DPWH ICT Inventory System")
        self.resize(1200, 750) # Slightly wider for a modern feel

        # --- MAIN STYLESHEET ---
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F3F4F6; /* Light gray background for main area */
            }
            QLabel {
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)

        # Central Widget & Main Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # ==========================================
        # 1. THE SIDEBAR (Dark Professional Theme)
        # ==========================================
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(240)
        self.sidebar.setStyleSheet("""
            QFrame {
                background-color: #1E293B; /* Deep slate blue */
                border-right: 1px solid #0F172A;
            }
            QPushButton {
                background-color: transparent;
                color: #94A3B8;
                text-align: left;
                padding: 12px 20px;
                font-size: 14px;
                font-family: 'Segoe UI', Arial;
                border: none;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #334155;
                color: #FFFFFF;
                border-left: 4px solid #3B82F6; /* Blue accent on hover */
            }
            QPushButton:checked {
                background-color: #0F172A;
                color: #3B82F6;
                border-left: 4px solid #3B82F6;
                font-weight: bold;
            }
        """)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(0, 20, 0, 20)
        self.sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Brand Title
        self.brand_label = QLabel("  DPWH ADMIN")
        self.brand_label.setStyleSheet("color: #FFFFFF; font-size: 20px; font-weight: bold; padding-left: 10px;")
        self.brand_sub = QLabel("    ICT Asset Management")
        self.brand_sub.setStyleSheet("color: #64748B; font-size: 12px; padding-left: 10px; margin-bottom: 20px;")
        
        self.sidebar_layout.addWidget(self.brand_label)
        self.sidebar_layout.addWidget(self.brand_sub)

        # Navigation Buttons (Using Unicode icons)
        self.btn_dashboard = QPushButton(" 📊  Dashboard")
        self.btn_personnel = QPushButton(" 👥  Personnel")
        self.btn_hardware = QPushButton(" 💻  Hardware")
        
        # Make buttons checkable so they stay "highlighted" when clicked
        for btn in [self.btn_dashboard, self.btn_personnel, self.btn_hardware]:
            btn.setCheckable(True)
            self.sidebar_layout.addWidget(btn)

        self.btn_dashboard.setChecked(True) # Set default active

        # ==========================================
        # 2. THE CONTENT AREA (Header + Stacked Widget)
        # ==========================================
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        # TOP HEADER
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

        # THE STACKED WIDGET (Where the pages swap)
        self.content_stack = QStackedWidget()
        self.setup_pages()

        # Assemble Content Area
        self.content_layout.addWidget(self.header)
        self.content_layout.addWidget(self.content_stack)

        # ==========================================
        # 3. ASSEMBLE MAIN LAYOUT
        # ==========================================
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.content_area)

        # Connect buttons to routing function
        self.btn_dashboard.clicked.connect(lambda: self.switch_page(0, self.btn_dashboard, "Dashboard Overview"))
        self.btn_personnel.clicked.connect(lambda: self.switch_page(1, self.btn_personnel, "Personnel Management"))
        self.btn_hardware.clicked.connect(lambda: self.switch_page(2, self.btn_hardware, "Hardware Inventory"))

    def setup_pages(self):
        # --- PAGE 1: DASHBOARD ---
        self.page_dashboard = QWidget()
        dash_layout = QVBoxLayout(self.page_dashboard)
        dash_layout.setContentsMargins(30, 30, 30, 30)
        dash_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Dashboard "Cards" (Visualizing data)
        grid_cards = QGridLayout()
        grid_cards.setSpacing(20)
        
        card1 = self.create_stat_card("Total Hardware", "142", "#3B82F6") # Blue
        card2 = self.create_stat_card("Active Personnel", "85", "#10B981")  # Green
        card3 = self.create_stat_card("For Repair", "12", "#EF4444")        # Red
        
        grid_cards.addWidget(card1, 0, 0)
        grid_cards.addWidget(card2, 0, 1)
        grid_cards.addWidget(card3, 0, 2)
        
        dash_layout.addLayout(grid_cards)

        # --- PAGE 2 & 3: PLACEHOLDERS ---
        self.page_personnel = QLabel("Personnel Table will go here.")
        self.page_personnel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_personnel.setStyleSheet("font-size: 16px; color: #6B7280;")

        self.page_hardware = QLabel("Hardware Table will go here.")
        self.page_hardware.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_hardware.setStyleSheet("font-size: 16px; color: #6B7280;")

        # Add to stack
        self.content_stack.addWidget(self.page_dashboard)
        self.content_stack.addWidget(self.page_personnel)
        self.content_stack.addWidget(self.page_hardware)

    def create_stat_card(self, title, value, color_hex):
        """Creates a modern UI 'Card' for the dashboard."""
        card = QFrame()
        card.setFixedHeight(120)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 8px;
                border-top: 4px solid {color_hex};
            }}
        """)
        
        # Add a subtle drop shadow
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
        """Handles page routing and updates active button state."""
        # Uncheck all buttons
        self.btn_dashboard.setChecked(False)
        self.btn_personnel.setChecked(False)
        self.btn_hardware.setChecked(False)
        
        # Check the clicked button
        button.setChecked(True)
        
        # Change page and title
        self.content_stack.setCurrentIndex(index)
        self.page_title.setText(title)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())