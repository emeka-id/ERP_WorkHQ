# ERPSuite Lite

A simple desktop ERP prototype built with Python Tkinter.

## Features
- Sign-in screen and post-login sign-out option
- Button navigation for Add Vendor, View Vendors, Invoices (AP / AR), and Posted Invoices
- Invoice management for AP and AR
- Invoice list with double-click to open invoice details
- Post invoices for payment processing
- Invoice filter to view all invoices or only posted invoices
- Dedicated Posted Invoices view
- Delete actions for vendors, invoices, and posted invoices

## Run
```bash
python app.py
```

## Build Windows .exe
On a Windows machine, run:

```bat
build_exe.bat
```

After the build succeeds, the executable will be created at:

```text
dist\ERPSuite Lite.exe
```

Copy `dist\ERPSuite Lite.exe` to your Desktop to launch the app directly from Desktop.
