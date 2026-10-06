# IMOSE CRM - Build Instructions for Windows .exe

## Prerequisites
Before building, make sure you have:
1. **Python 3.9 or higher** installed ([Download here](https://www.python.org/downloads/))
   - Make sure to check "Add Python to PATH" during installation
2. **Git** installed (optional, for cloning the repository)

## Step 1: Prepare Your Computer

### Install Python
1. Download Python 3.9+ from https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT**: Check the box that says "Add Python to PATH"
4. Click "Install Now"
5. Verify installation by opening Command Prompt and typing:
   ```
   python --version
   ```

### Install Git (Optional)
1. Download from https://git-scm.com/download/win
2. Run the installer with default settings

## Step 2: Clone and Setup the Project

### Option A: Using Command Prompt (Recommended)
1. Open **Command Prompt** (Press Windows key + R, type `cmd`, press Enter)
2. Navigate to where you want to save the project:
   ```
   cd Desktop
   ```
3. Clone the repository:
   ```
   git clone https://github.com/Olayiwoladansa/mobile-repair-app.git
   cd mobile-repair-app
   ```

### Option B: Manual Download
1. Visit https://github.com/Olayiwoladansa/mobile-repair-app
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file to your desired location
4. Open Command Prompt and navigate to the extracted folder

## Step 3: Install Dependencies

1. Open Command Prompt in the project folder
2. Run:
   ```
   pip install -r requirements.txt
   ```
   This will install:
   - PyQt5 (User Interface)
   - PyInstaller (EXE Builder)
   - ReportLab (PDF/Invoice Generation)
   - And other required packages

## Step 4: Build the .exe

### Automatic Build (Easiest)
1. In the project folder, double-click `build_exe.bat`
2. Wait for the build to complete (takes 2-5 minutes)
3. Your .exe file will be in the `dist` folder

### Manual Build
1. Open Command Prompt in the project folder
2. Run:
   ```
   pyinstaller --onefile --windowed --name "IMOSE_CRM" main.py
   ```
3. Wait for completion
4. Your .exe will be in `dist/IMOSE_CRM.exe`

## Step 5: Run the Application

### First Time
1. Navigate to the `dist` folder
2. Double-click `IMOSE_CRM.exe`
3. The app will launch
4. **Default Login:**
   - Username: `admin`
   - Password: `admin123`

### Create a Shortcut (Optional)
1. Right-click `IMOSE_CRM.exe`
2. Select "Create Shortcut"
3. Move shortcut to Desktop for easy access

## Step 6: Installation (Optional)

To make installation easier for others, you can create an installer:

1. Install NSIS: https://nsis.sourceforge.io/download
2. In the project folder, create `installer.nsi` with installer configuration
3. Right-click `installer.nsi` → "Compile NSIS Script"
4. This creates an `.exe` installer that users can run

## Troubleshooting

### Problem: "Python is not recognized"
**Solution:** 
1. Reinstall Python and check "Add Python to PATH"
2. Restart Command Prompt after installation

### Problem: "pip is not found"
**Solution:**
```
python -m pip install --upgrade pip
```

### Problem: "PyQt5 not found" error when running .exe
**Solution:** This shouldn't happen with PyInstaller. Rebuild using:
```
pyinstaller --onefile --windowed --collect-all PyQt5 main.py
```

### Problem: .exe crashes on startup
**Solution:** 
1. Check you're using Python 3.9 or higher
2. Rebuild with verbose output:
   ```
   pyinstaller --onefile --windowed --debug=imports main.py
   ```

## Updating the Database

The app stores data in `imose_crm.db` (SQLite database).
- On first run, the database is automatically created
- Data persists between app sessions
- To reset, delete `imose_crm.db` and restart the app

## Features Available

✅ Admin Dashboard:
- Customer Management
- Repair Ticket Creation & Status Tracking
- Parts Inventory Management
- Invoice & Payment Tracking
- Technician Assignment

✅ Customer Portal:
- View repair requests
- Track repair status

## Need Help?

1. Check GitHub Issues: https://github.com/Olayiwoladansa/mobile-repair-app/issues
2. Review error messages carefully
3. Ensure all dependencies are installed: `pip install -r requirements.txt`

## Next Steps

After building:
1. Test the application thoroughly
2. Create additional user accounts
3. Customize the database as needed
4. Share the .exe with team members

---

**Ready to build?** Run `build_exe.bat` or follow the manual steps above!
