from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
                             QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
                             QDialog, QFormLayout, QComboBox, QSpinBox, QDoubleSpinBox, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database import Database
from datetime import datetime

class AdminDashboard(QMainWindow):
    def __init__(self, user_id, username):
        super().__init__()
        self.user_id = user_id
        self.username = username
        self.db = Database()
        self.db.connect()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(f'IMOSE CRM - Admin Dashboard ({self.username})')
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet("background-color: #f5f5f5;")
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Header
        header = QLabel('IMOSE CRM - Admin Dashboard')
        header_font = QFont()
        header_font.setPointSize(18)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setStyleSheet("padding: 10px; background-color: #007bff; color: white;")
        main_layout.addWidget(header)
        
        # Tab widget
        tabs = QTabWidget()
        
        # Dashboard tab
        tabs.addTab(self.create_dashboard_tab(), 'Dashboard')
        # Customers tab
        tabs.addTab(self.create_customers_tab(), 'Customers')
        # Repair Tickets tab
        tabs.addTab(self.create_repair_tickets_tab(), 'Repair Tickets')
        # Inventory tab
        tabs.addTab(self.create_inventory_tab(), 'Parts Inventory')
        # Invoices tab
        tabs.addTab(self.create_invoices_tab(), 'Invoices')
        # Technicians tab
        tabs.addTab(self.create_technicians_tab(), 'Technicians')
        
        main_layout.addWidget(tabs)
        
        # Logout button
        logout_button = QPushButton('Logout')
        logout_button.setStyleSheet("background-color: #dc3545; color: white; padding: 10px;")
        logout_button.clicked.connect(self.logout)
        main_layout.addWidget(logout_button)
        
        central_widget.setLayout(main_layout)
    
    def create_dashboard_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Statistics
        stats_layout = QHBoxLayout()
        
        # Total customers
        customers = self.db.fetch_all('SELECT COUNT(*) FROM customers')
        customer_label = QLabel(f"Total Customers: {customers[0][0]}")
        customer_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px; background-color: white; border-radius: 4px;")
        stats_layout.addWidget(customer_label)
        
        # Pending repairs
        repairs = self.db.fetch_all("SELECT COUNT(*) FROM repair_tickets WHERE status = 'Pending'")
        repair_label = QLabel(f"Pending Repairs: {repairs[0][0]}")
        repair_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px; background-color: white; border-radius: 4px;")
        stats_layout.addWidget(repair_label)
        
        # Unpaid invoices
        invoices = self.db.fetch_all("SELECT COUNT(*) FROM invoices WHERE payment_status = 'Unpaid'")
        invoice_label = QLabel(f"Unpaid Invoices: {invoices[0][0]}")
        invoice_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px; background-color: white; border-radius: 4px;")
        stats_layout.addWidget(invoice_label)
        
        layout.addLayout(stats_layout)
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_customers_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Add customer button
        add_btn = QPushButton('Add New Customer')
        add_btn.setStyleSheet("background-color: #28a745; color: white; padding: 10px;")
        add_btn.clicked.connect(self.add_customer)
        layout.addWidget(add_btn)
        
        # Table
        self.customers_table = QTableWidget()
        self.customers_table.setColumnCount(5)
        self.customers_table.setHorizontalHeaderLabels(['ID', 'Name', 'Phone', 'Email', 'Actions'])
        self.refresh_customers_table()
        layout.addWidget(self.customers_table)
        
        widget.setLayout(layout)
        return widget
    
    def refresh_customers_table(self):
        customers = self.db.fetch_all('SELECT * FROM customers')
        self.customers_table.setRowCount(len(customers))
        
        for row, customer in enumerate(customers):
            self.customers_table.setItem(row, 0, QTableWidgetItem(str(customer[0])))
            self.customers_table.setItem(row, 1, QTableWidgetItem(customer[1]))
            self.customers_table.setItem(row, 2, QTableWidgetItem(customer[2]))
            self.customers_table.setItem(row, 3, QTableWidgetItem(customer[3] or ''))
            
            # Actions button
            delete_btn = QPushButton('Delete')
            delete_btn.clicked.connect(lambda checked, cid=customer[0]: self.delete_customer(cid))
            self.customers_table.setCellWidget(row, 4, delete_btn)
    
    def add_customer(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Add Customer')
        dialog.setGeometry(200, 200, 400, 300)
        
        form_layout = QFormLayout()
        
        name_input = QLineEdit()
        phone_input = QLineEdit()
        email_input = QLineEdit()
        address_input = QLineEdit()
        
        form_layout.addRow('Name:', name_input)
        form_layout.addRow('Phone:', phone_input)
        form_layout.addRow('Email:', email_input)
        form_layout.addRow('Address:', address_input)
        
        save_btn = QPushButton('Save')
        save_btn.clicked.connect(lambda: self.save_customer(name_input, phone_input, email_input, address_input, dialog))
        form_layout.addWidget(save_btn)
        
        dialog.setLayout(form_layout)
        dialog.exec_()
    
    def save_customer(self, name_input, phone_input, email_input, address_input, dialog):
        name = name_input.text().strip()
        phone = phone_input.text().strip()
        email = email_input.text().strip()
        address = address_input.text().strip()
        
        if not name or not phone:
            QMessageBox.warning(dialog, 'Error', 'Name and Phone are required')
            return
        
        self.db.execute(
            'INSERT INTO customers (name, phone, email, address) VALUES (?, ?, ?, ?)',
            (name, phone, email, address)
        )
        QMessageBox.information(dialog, 'Success', 'Customer added successfully')
        dialog.close()
        self.refresh_customers_table()
    
    def delete_customer(self, customer_id):
        reply = QMessageBox.question(self, 'Confirm', 'Delete this customer?', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
            self.refresh_customers_table()
    
    def create_repair_tickets_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        add_btn = QPushButton('Create Repair Ticket')
        add_btn.setStyleSheet("background-color: #28a745; color: white; padding: 10px;")
        add_btn.clicked.connect(self.create_repair_ticket)
        layout.addWidget(add_btn)
        
        self.tickets_table = QTableWidget()
        self.tickets_table.setColumnCount(6)
        self.tickets_table.setHorizontalHeaderLabels(['ID', 'Customer', 'Device', 'Issue', 'Status', 'Actions'])
        self.refresh_tickets_table()
        layout.addWidget(self.tickets_table)
        
        widget.setLayout(layout)
        return widget
    
    def refresh_tickets_table(self):
        tickets = self.db.fetch_all('''
            SELECT rt.id, c.name, rt.device_type, rt.issue_description, rt.status
            FROM repair_tickets rt
            JOIN customers c ON rt.customer_id = c.id
        ''')
        self.tickets_table.setRowCount(len(tickets))
        
        for row, ticket in enumerate(tickets):
            self.tickets_table.setItem(row, 0, QTableWidgetItem(str(ticket[0])))
            self.tickets_table.setItem(row, 1, QTableWidgetItem(ticket[1]))
            self.tickets_table.setItem(row, 2, QTableWidgetItem(ticket[2]))
            self.tickets_table.setItem(row, 3, QTableWidgetItem(ticket[3] or ''))
            self.tickets_table.setItem(row, 4, QTableWidgetItem(ticket[4]))
            
            status_btn = QPushButton('Update Status')
            status_btn.clicked.connect(lambda checked, tid=ticket[0]: self.update_ticket_status(tid))
            self.tickets_table.setCellWidget(row, 5, status_btn)
    
    def create_repair_ticket(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Create Repair Ticket')
        dialog.setGeometry(200, 200, 400, 400)
        
        form_layout = QFormLayout()
        
        # Get customers
        customers = self.db.fetch_all('SELECT id, name FROM customers')
        customer_combo = QComboBox()
        for cid, cname in customers:
            customer_combo.addItem(cname, cid)
        
        device_input = QLineEdit()
        model_input = QLineEdit()
        issue_input = QLineEdit()
        
        form_layout.addRow('Customer:', customer_combo)
        form_layout.addRow('Device Type:', device_input)
        form_layout.addRow('Device Model:', model_input)
        form_layout.addRow('Issue Description:', issue_input)
        
        save_btn = QPushButton('Create')
        save_btn.clicked.connect(lambda: self.save_ticket(customer_combo, device_input, model_input, issue_input, dialog))
        form_layout.addWidget(save_btn)
        
        dialog.setLayout(form_layout)
        dialog.exec_()
    
    def save_ticket(self, customer_combo, device_input, model_input, issue_input, dialog):
        customer_id = customer_combo.currentData()
        device = device_input.text().strip()
        model = model_input.text().strip()
        issue = issue_input.text().strip()
        
        if not customer_id or not device:
            QMessageBox.warning(dialog, 'Error', 'Customer and Device Type are required')
            return
        
        self.db.execute(
            'INSERT INTO repair_tickets (customer_id, device_type, device_model, issue_description, status) VALUES (?, ?, ?, ?, ?)',
            (customer_id, device, model, issue, 'Pending')
        )
        QMessageBox.information(dialog, 'Success', 'Repair ticket created')
        dialog.close()
        self.refresh_tickets_table()
    
    def update_ticket_status(self, ticket_id):
        dialog = QDialog(self)
        dialog.setWindowTitle('Update Ticket Status')
        dialog.setGeometry(200, 200, 300, 200)
        
        form_layout = QFormLayout()
        
        status_combo = QComboBox()
        status_combo.addItems(['Pending', 'In Progress', 'Completed', 'On Hold'])
        
        form_layout.addRow('Status:', status_combo)
        
        save_btn = QPushButton('Update')
        save_btn.clicked.connect(lambda: self.save_ticket_status(ticket_id, status_combo.currentText(), dialog))
        form_layout.addWidget(save_btn)
        
        dialog.setLayout(form_layout)
        dialog.exec_()
    
    def save_ticket_status(self, ticket_id, status, dialog):
        self.db.execute('UPDATE repair_tickets SET status = ? WHERE id = ?', (status, ticket_id))
        QMessageBox.information(dialog, 'Success', 'Status updated')
        dialog.close()
        self.refresh_tickets_table()
    
    def create_inventory_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        add_btn = QPushButton('Add Part')
        add_btn.setStyleSheet("background-color: #28a745; color: white; padding: 10px;")
        add_btn.clicked.connect(self.add_part)
        layout.addWidget(add_btn)
        
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(6)
        self.inventory_table.setHorizontalHeaderLabels(['Part Name', 'Code', 'Quantity', 'Unit Price', 'Supplier', 'Actions'])
        self.refresh_inventory_table()
        layout.addWidget(self.inventory_table)
        
        widget.setLayout(layout)
        return widget
    
    def refresh_inventory_table(self):
        parts = self.db.fetch_all('SELECT * FROM inventory')
        self.inventory_table.setRowCount(len(parts))
        
        for row, part in enumerate(parts):
            self.inventory_table.setItem(row, 0, QTableWidgetItem(part[1]))
            self.inventory_table.setItem(row, 1, QTableWidgetItem(part[2] or ''))
            self.inventory_table.setItem(row, 2, QTableWidgetItem(str(part[3])))
            self.inventory_table.setItem(row, 3, QTableWidgetItem(str(part[4] or '')))
            self.inventory_table.setItem(row, 4, QTableWidgetItem(part[5] or ''))
            
            delete_btn = QPushButton('Delete')
            delete_btn.clicked.connect(lambda checked, pid=part[0]: self.delete_part(pid))
            self.inventory_table.setCellWidget(row, 5, delete_btn)
    
    def add_part(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Add Part')
        dialog.setGeometry(200, 200, 400, 300)
        
        form_layout = QFormLayout()
        
        name_input = QLineEdit()
        code_input = QLineEdit()
        quantity_input = QSpinBox()
        price_input = QDoubleSpinBox()
        supplier_input = QLineEdit()
        
        form_layout.addRow('Part Name:', name_input)
        form_layout.addRow('Part Code:', code_input)
        form_layout.addRow('Quantity:', quantity_input)
        form_layout.addRow('Unit Price:', price_input)
        form_layout.addRow('Supplier:', supplier_input)
        
        save_btn = QPushButton('Save')
        save_btn.clicked.connect(lambda: self.save_part(name_input, code_input, quantity_input, price_input, supplier_input, dialog))
        form_layout.addWidget(save_btn)
        
        dialog.setLayout(form_layout)
        dialog.exec_()
    
    def save_part(self, name_input, code_input, quantity_input, price_input, supplier_input, dialog):
        name = name_input.text().strip()
        code = code_input.text().strip()
        quantity = quantity_input.value()
        price = price_input.value()
        supplier = supplier_input.text().strip()
        
        if not name:
            QMessageBox.warning(dialog, 'Error', 'Part Name is required')
            return
        
        self.db.execute(
            'INSERT INTO inventory (part_name, part_code, quantity, unit_price, supplier) VALUES (?, ?, ?, ?, ?)',
            (name, code, quantity, price, supplier)
        )
        QMessageBox.information(dialog, 'Success', 'Part added')
        dialog.close()
        self.refresh_inventory_table()
    
    def delete_part(self, part_id):
        reply = QMessageBox.question(self, 'Confirm', 'Delete this part?', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.execute('DELETE FROM inventory WHERE id = ?', (part_id,))
            self.refresh_inventory_table()
    
    def create_invoices_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.invoices_table = QTableWidget()
        self.invoices_table.setColumnCount(6)
        self.invoices_table.setHorizontalHeaderLabels(['Invoice ID', 'Customer', 'Amount', 'Status', 'Payment Method', 'Actions'])
        self.refresh_invoices_table()
        layout.addWidget(self.invoices_table)
        
        widget.setLayout(layout)
        return widget
    
    def refresh_invoices_table(self):
        invoices = self.db.fetch_all('''
            SELECT i.id, c.name, i.total_amount, i.payment_status, i.payment_method
            FROM invoices i
            JOIN customers c ON i.customer_id = c.id
        ''')
        self.invoices_table.setRowCount(len(invoices))
        
        for row, invoice in enumerate(invoices):
            self.invoices_table.setItem(row, 0, QTableWidgetItem(str(invoice[0])))
            self.invoices_table.setItem(row, 1, QTableWidgetItem(invoice[1]))
            self.invoices_table.setItem(row, 2, QTableWidgetItem(f"${invoice[2]:.2f}"))
            self.invoices_table.setItem(row, 3, QTableWidgetItem(invoice[3]))
            self.invoices_table.setItem(row, 4, QTableWidgetItem(invoice[4] or ''))
            
            mark_btn = QPushButton('Mark Paid')
            mark_btn.clicked.connect(lambda checked, iid=invoice[0]: self.mark_paid(iid))
            self.invoices_table.setCellWidget(row, 5, mark_btn)
    
    def mark_paid(self, invoice_id):
        self.db.execute('UPDATE invoices SET payment_status = ? WHERE id = ?', ('Paid', invoice_id))
        self.refresh_invoices_table()
    
    def create_technicians_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        label = QLabel('Technician Management')
        layout.addWidget(label)
        
        self.technicians_table = QTableWidget()
        self.technicians_table.setColumnCount(4)
        self.technicians_table.setHorizontalHeaderLabels(['ID', 'Name', 'Specialization', 'Phone'])
        self.refresh_technicians_table()
        layout.addWidget(self.technicians_table)
        
        widget.setLayout(layout)
        return widget
    
    def refresh_technicians_table(self):
        technicians = self.db.fetch_all('''
            SELECT t.id, u.username, t.specialization, t.phone
            FROM technicians t
            JOIN users u ON t.user_id = u.id
        ''')
        self.technicians_table.setRowCount(len(technicians))
        
        for row, tech in enumerate(technicians):
            self.technicians_table.setItem(row, 0, QTableWidgetItem(str(tech[0])))
            self.technicians_table.setItem(row, 1, QTableWidgetItem(tech[1]))
            self.technicians_table.setItem(row, 2, QTableWidgetItem(tech[2] or ''))
            self.technicians_table.setItem(row, 3, QTableWidgetItem(tech[3] or ''))
    
    def logout(self):
        self.db.close()
        self.close()
