from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from database import Database
import hashlib
from gui.admin_dashboard import AdminDashboard
from gui.customer_dashboard import CustomerDashboard

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.db.connect()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('IMOSE CRM - Login')
        self.setGeometry(100, 100, 500, 400)
        self.setStyleSheet("background-color: #f0f0f0;")
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(50, 50, 50, 50)
        
        # Title
        title = QLabel('IMOSE CRM')
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel('Mobile Phone Repair Customer Service')
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #666;")
        main_layout.addWidget(subtitle)
        
        # Username
        username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.username_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")
        main_layout.addWidget(username_label)
        main_layout.addWidget(self.username_input)
        
        # Password
        password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")
        main_layout.addWidget(password_label)
        main_layout.addWidget(self.password_input)
        
        # Login button
        login_button = QPushButton('Login')
        login_button.setStyleSheet("""\n            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        login_button.clicked.connect(self.login)
        main_layout.addWidget(login_button)
        
        # Info label
        info_label = QLabel('Default: admin / admin123')
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("color: #999; font-size: 10px;")
        main_layout.addWidget(info_label)
        
        main_layout.addStretch()
        central_widget.setLayout(main_layout)
    
    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter username and password')
            return
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = self.db.fetch_one(
            'SELECT * FROM users WHERE username = ? AND password = ?',
            (username, hashed_password)
        )
        
        if user:
            user_id = user[0]
            role = user[4]
            
            if role == 'admin':
                self.open_admin_dashboard(user_id, username)
            else:
                self.open_customer_dashboard(user_id, username)
            self.close()
        else:
            QMessageBox.critical(self, 'Error', 'Invalid username or password')
    
    def open_admin_dashboard(self, user_id, username):
        self.admin_dashboard = AdminDashboard(user_id, username)
        self.admin_dashboard.show()
    
    def open_customer_dashboard(self, user_id, username):
        self.customer_dashboard = CustomerDashboard(user_id, username)
        self.customer_dashboard.show()
    
    def closeEvent(self, event):
        self.db.close()
        event.accept()
