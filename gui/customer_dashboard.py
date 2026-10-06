from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont
from database import Database

class CustomerDashboard(QMainWindow):
    def __init__(self, user_id, username):
        super().__init__()
        self.user_id = user_id
        self.username = username
        self.db = Database()
        self.db.connect()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(f'IMOSE CRM - Customer Portal ({self.username})')
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("background-color: #f5f5f5;")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Header
        header = QLabel('My Repair Requests')
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setStyleSheet("padding: 10px; background-color: #007bff; color: white;")
        layout.addWidget(header)
        
        # Table of repair tickets
        self.tickets_table = QTableWidget()
        self.tickets_table.setColumnCount(5)
        self.tickets_table.setHorizontalHeaderLabels(['Ticket ID', 'Device', 'Issue', 'Status', 'Created'])
        self.refresh_table()
        layout.addWidget(self.tickets_table)
        
        # Logout button
        logout_button = QPushButton('Logout')
        logout_button.setStyleSheet("background-color: #dc3545; color: white; padding: 10px;")
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button)
        
        central_widget.setLayout(layout)
    
    def refresh_table(self):
        # Fetch repair tickets for this user
        tickets = self.db.fetch_all('''
            SELECT id, device_type, issue_description, status, created_at
            FROM repair_tickets
            LIMIT 20
        ''')
        
        self.tickets_table.setRowCount(len(tickets))
        for row, ticket in enumerate(tickets):
            self.tickets_table.setItem(row, 0, QTableWidgetItem(str(ticket[0])))
            self.tickets_table.setItem(row, 1, QTableWidgetItem(ticket[1]))
            self.tickets_table.setItem(row, 2, QTableWidgetItem(ticket[2] or ''))
            self.tickets_table.setItem(row, 3, QTableWidgetItem(ticket[3]))
            self.tickets_table.setItem(row, 4, QTableWidgetItem(str(ticket[4])))
    
    def logout(self):
        self.db.close()
        self.close()
