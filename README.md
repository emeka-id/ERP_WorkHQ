# ERPSuite Lite

A simple desktop ERP prototype built with Python Tkinter.

## Features
- Sign-in screen and post-login sign-out option
- Blue Prism-friendly native button navigation for Add Vendor, View Vendors, Invoices (AP / AR), and Posted Invoices
- Invoice management for AP and AR
- Invoice list with double-click to open invoice details
- Post invoices for payment processing
- Invoice filter to view all invoices or only posted invoices
- Dedicated Posted Invoices view
- Delete actions for vendors, invoices, and posted invoices

## Automation Notes
The main navigation controls are classic Tk buttons with stable widget names for Windows automation tools such as Blue Prism:

- `nav_add_vendor_button` - Add Vendor
- `nav_view_vendors_button` - View Vendors
- `nav_invoices_ap_ar_button` - Invoices (AP / AR)
- `nav_posted_invoices_button` - Posted Invoices

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
