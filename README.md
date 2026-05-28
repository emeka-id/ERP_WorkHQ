# ERPSuite Lite

A simple desktop ERP prototype built with Python and PySide6.

## Features
- Sign-in screen and post-login sign-out option
- Blue Prism-friendly Qt button navigation for Add Vendor, View Vendors, Invoices (AP / AR), and Posted Invoices
- Invoice management for AP and AR
- Invoice list with double-click to open invoice details
- Post invoices for payment processing
- Invoice filter to view all invoices or only posted invoices
- Dedicated Posted Invoices view
- Delete actions for vendors, invoices, and posted invoices

## Automation Notes
The main navigation controls are PySide6 `QPushButton` widgets with stable `objectName` values for Windows automation tools such as Blue Prism:

- `nav_add_vendor_button` - Add Vendor
- `nav_view_vendors_button` - View Vendors
- `nav_invoices_ap_ar_button` - Invoices (AP / AR)
- `nav_posted_invoices_button` - Posted Invoices

Other important automation IDs include:

- `sign_in_button` and `sign_out_button`
- `vendor_table`
- `invoice_table`
- `posted_invoice_table`
- `invoice_vendor_combo`

## Install Dependencies
```bash
python -m pip install -r requirements.txt
```

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
