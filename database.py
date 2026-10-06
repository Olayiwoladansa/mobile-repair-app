import sqlite3
import os
from datetime import datetime
import hashlib

class Database:
    def __init__(self, db_name='imose_crm.db'):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Connect to database"""
        self.connection = sqlite3.connect(self.db_name)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
    
    def initialize(self):
        """Create all tables"""
        self.connect()
        
        # Users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT,
                role TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Customers table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Repair Tickets table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS repair_tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                device_type TEXT NOT NULL,
                device_model TEXT,
                issue_description TEXT,
                status TEXT DEFAULT 'Pending',
                assigned_technician_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY(customer_id) REFERENCES customers(id),
                FOREIGN KEY(assigned_technician_id) REFERENCES users(id)
            )
        ''')
        
        # Parts Inventory table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                part_name TEXT NOT NULL,
                part_code TEXT UNIQUE,
                quantity INTEGER DEFAULT 0,
                unit_price REAL,
                supplier TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Invoices table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id INTEGER NOT NULL,
                customer_id INTEGER NOT NULL,
                labor_cost REAL,
                parts_cost REAL,
                total_amount REAL,
                payment_status TEXT DEFAULT 'Unpaid',
                payment_method TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(ticket_id) REFERENCES repair_tickets(id),
                FOREIGN KEY(customer_id) REFERENCES customers(id)
            )
        ''')
        
        # Technicians table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS technicians (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                specialization TEXT,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        
        # Create default admin user if not exists
        try:
            hashed_password = hashlib.sha256('admin123'.encode()).hexdigest()
            self.cursor.execute('''
                INSERT INTO users (username, password, email, role)
                VALUES (?, ?, ?, ?)
            ''', ('admin', hashed_password, 'admin@imosecrm.com', 'admin'))
        except sqlite3.IntegrityError:
            pass  # User already exists
        
        self.connection.commit()
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
    
    def execute(self, query, params=None):
        """Execute a query"""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.connection.commit()
    
    def fetch_one(self, query, params=None):
        """Fetch one record"""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchone()
    
    def fetch_all(self, query, params=None):
        """Fetch all records"""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()
