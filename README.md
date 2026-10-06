# Mobile Phone Repair Customer Service App

A complete desktop application for managing mobile phone repair operations.

## Features

- **Customer Management**: Register and manage customer accounts
- **Repair Tickets**: Create and track repair requests
- **Device Information**: Store device details, issue descriptions, and diagnostics
- **Status Tracking**: Real-time repair status updates
- **Parts Inventory**: Manage repair parts and stock levels
- **Technician Assignment**: Assign repair jobs to technicians
- **Payment & Invoicing**: Create invoices and track payments
- **Admin Dashboard**: Comprehensive business analytics and management

## Installation (Windows .exe)

1. Download the latest .exe installer from the releases page
2. Run the installer
3. Follow the setup wizard
4. Launch the app and log in

## Getting Started (Development)

### Requirements
- Python 3.9+
- pip (Python package manager)

### Setup
```bash
# Clone the repository
git clone https://github.com/Olayiwoladansa/mobile-repair-app.git
cd mobile-repair-app

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Building .exe Installer

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed main.py

# The .exe will be in the dist/ folder
```

## Default Credentials (First Login)

- **Username**: admin
- **Password**: admin123

⚠️ Change these immediately after first login!

## Project Structure

```
mobile-repair-app/
├── main.py                 # Application entry point
├── database.py             # Database setup and models
├── gui/
│   ├── login_window.py     # Login interface
│   ├── customer_dashboard.py # Customer interface
│   ├── admin_dashboard.py  # Admin interface
│   └── repair_tickets.py   # Repair ticket management
├── modules/
│   ├── customer.py         # Customer management
│   ├── repairs.py          # Repair ticket logic
│   ├── inventory.py        # Parts inventory
│   ├── invoicing.py        # Invoice generation
│   └── reporting.py        # Business reports
└── requirements.txt        # Dependencies
```

## Support

For issues or feature requests, please create an issue on GitHub.
