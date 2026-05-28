import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QFormLayout,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


@dataclass
class Vendor:
    id: int
    name: str
    email: str
    phone: str


@dataclass
class Invoice:
    id: int
    invoice_number: str
    invoice_type: str
    vendor_id: int
    amount: float
    due_date: str
    notes: str
    status: str = "Draft"


class ERPSuiteLiteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ERPSuite Lite")
        self.resize(1100, 700)

        self.vendors: list[Vendor] = []
        self.invoices: list[Invoice] = []
        self.next_vendor_id = 1
        self.next_invoice_id = 1
        self.navigation_buttons: dict[QWidget, QPushButton] = {}

        self._build_login()

    def _build_login(self):
        login_widget = QWidget(objectName="login_page")
        layout = QVBoxLayout(login_widget)
        layout.setAlignment(Qt.AlignCenter)

        card = QGroupBox("Sign In", objectName="sign_in_group")
        card_layout = QFormLayout(card)

        self.username_entry = QLineEdit(objectName="username_entry")
        self.password_entry = QLineEdit(objectName="password_entry")
        self.password_entry.setEchoMode(QLineEdit.Password)

        sign_in_button = QPushButton("Sign In", objectName="sign_in_button")
        sign_in_button.clicked.connect(self.sign_in)

        card_layout.addRow("Username", self.username_entry)
        card_layout.addRow("Password", self.password_entry)
        card_layout.addRow(sign_in_button)
        card_layout.addRow(QLabel("Please enter your username/password", objectName="login_instruction_label"))

        layout.addWidget(card)
        self.setCentralWidget(login_widget)

    def sign_in(self):
        self._build_main_ui()

    def _build_main_ui(self):
        main_widget = QWidget(objectName="main_page")
        main_layout = QVBoxLayout(main_widget)

        top_bar = QHBoxLayout()
        top_bar.addStretch()
        sign_out_button = QPushButton("Sign Out", objectName="sign_out_button")
        sign_out_button.clicked.connect(self.sign_out)
        top_bar.addWidget(sign_out_button)
        main_layout.addLayout(top_bar)

        nav_frame = QFrame(objectName="navigation_frame")
        nav_layout = QHBoxLayout(nav_frame)
        nav_layout.setContentsMargins(0, 0, 0, 0)

        self.content_stack = QStackedWidget(objectName="content_stack")
        self.add_vendor_page = QWidget(objectName="add_vendor_page")
        self.view_vendors_page = QWidget(objectName="view_vendors_page")
        self.invoices_page = QWidget(objectName="invoices_ap_ar_page")
        self.posted_invoices_page = QWidget(objectName="posted_invoices_page")

        self.navigation_buttons = {
            self.add_vendor_page: self._create_navigation_button("Add Vendor", "nav_add_vendor_button", self.add_vendor_page),
            self.view_vendors_page: self._create_navigation_button("View Vendors", "nav_view_vendors_button", self.view_vendors_page),
            self.invoices_page: self._create_navigation_button("Invoices (AP / AR)", "nav_invoices_ap_ar_button", self.invoices_page),
            self.posted_invoices_page: self._create_navigation_button("Posted Invoices", "nav_posted_invoices_button", self.posted_invoices_page),
        }
        for button in self.navigation_buttons.values():
            nav_layout.addWidget(button)
        nav_layout.addStretch()

        main_layout.addWidget(nav_frame)
        main_layout.addWidget(self.content_stack)

        self._build_add_vendor_page()
        self._build_view_vendors_page()
        self._build_invoices_page()
        self._build_posted_invoices_page()
        self.refresh_invoice_tables()

        for page in (self.add_vendor_page, self.view_vendors_page, self.invoices_page, self.posted_invoices_page):
            self.content_stack.addWidget(page)

        self.show_section(self.add_vendor_page)
        self.setCentralWidget(main_widget)

    def _create_navigation_button(self, label: str, object_name: str, section: QWidget) -> QPushButton:
        button = QPushButton(label, objectName=object_name)
        button.setCheckable(True)
        button.setFocusPolicy(Qt.StrongFocus)
        button.clicked.connect(lambda: self.show_section(section))
        return button

    def show_section(self, section: QWidget):
        self.content_stack.setCurrentWidget(section)
        for page, button in self.navigation_buttons.items():
            button.setChecked(page is section)

    def sign_out(self):
        self._build_login()

    def _build_add_vendor_page(self):
        layout = QVBoxLayout(self.add_vendor_page)
        form_group = QGroupBox("Add New Vendor", objectName="add_vendor_group")
        form_layout = QGridLayout(form_group)

        self.vendor_name_entry = QLineEdit(objectName="vendor_name_entry")
        self.vendor_email_entry = QLineEdit(objectName="vendor_email_entry")
        self.vendor_phone_entry = QLineEdit(objectName="vendor_phone_entry")
        add_button = QPushButton("Add Vendor", objectName="add_vendor_button")
        add_button.clicked.connect(self.add_vendor)

        form_layout.addWidget(QLabel("Name"), 0, 0)
        form_layout.addWidget(self.vendor_name_entry, 0, 1)
        form_layout.addWidget(QLabel("Email"), 0, 2)
        form_layout.addWidget(self.vendor_email_entry, 0, 3)
        form_layout.addWidget(QLabel("Phone"), 0, 4)
        form_layout.addWidget(self.vendor_phone_entry, 0, 5)
        form_layout.addWidget(add_button, 0, 6)

        layout.addWidget(form_group)
        layout.addStretch()

    def _build_view_vendors_page(self):
        layout = QVBoxLayout(self.view_vendors_page)
        group = QGroupBox("Vendors", objectName="vendors_group")
        group_layout = QVBoxLayout(group)

        self.vendor_table = self._create_table("vendor_table", ["ID", "NAME", "EMAIL", "PHONE"])
        group_layout.addWidget(self.vendor_table)
        for vendor in self.vendors:
            self._add_vendor_table_row(vendor)

        delete_button = QPushButton("Delete Selected Vendor", objectName="delete_vendor_button")
        delete_button.clicked.connect(self.delete_selected_vendor)

        layout.addWidget(group)
        layout.addWidget(delete_button, alignment=Qt.AlignRight)

    def _build_invoices_page(self):
        layout = QVBoxLayout(self.invoices_page)
        form_group = QGroupBox("Create Invoice", objectName="create_invoice_group")
        form_layout = QGridLayout(form_group)

        self.inv_num_entry = QLineEdit(objectName="invoice_number_entry")
        self.inv_type = QComboBox(objectName="invoice_type_combo")
        self.inv_type.addItems(["AP", "AR"])
        self.vendor_choice = QComboBox(objectName="invoice_vendor_combo")
        self.vendor_choice.setEditable(True)
        self.inv_amount_entry = QLineEdit(objectName="invoice_amount_entry")
        self.inv_due_entry = QLineEdit(datetime.today().strftime("%Y-%m-%d"), objectName="invoice_due_date_entry")
        self.inv_notes_entry = QLineEdit(objectName="invoice_notes_entry")

        save_button = QPushButton("Save Invoice", objectName="save_invoice_button")
        save_button.clicked.connect(self.add_invoice)
        post_button = QPushButton("Post Selected Invoice", objectName="post_invoice_button")
        post_button.clicked.connect(self.post_selected_invoice)

        form_layout.addWidget(QLabel("Invoice #"), 0, 0)
        form_layout.addWidget(self.inv_num_entry, 0, 1)
        form_layout.addWidget(QLabel("Type"), 0, 2)
        form_layout.addWidget(self.inv_type, 0, 3)
        form_layout.addWidget(QLabel("Vendor"), 0, 4)
        form_layout.addWidget(self.vendor_choice, 0, 5)
        form_layout.addWidget(QLabel("Amount"), 1, 0)
        form_layout.addWidget(self.inv_amount_entry, 1, 1)
        form_layout.addWidget(QLabel("Due Date (YYYY-MM-DD)"), 1, 2)
        form_layout.addWidget(self.inv_due_entry, 1, 3)
        form_layout.addWidget(QLabel("Notes"), 1, 4)
        form_layout.addWidget(self.inv_notes_entry, 1, 5)
        form_layout.addWidget(save_button, 2, 0, 1, 2)
        form_layout.addWidget(post_button, 2, 2, 1, 2)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Invoice View:"))
        self.invoice_filter = QComboBox(objectName="invoice_filter_combo")
        self.invoice_filter.addItems(["All", "Posted"])
        self.invoice_filter.currentTextChanged.connect(self.filter_invoices)
        filter_layout.addWidget(self.invoice_filter)
        filter_layout.addStretch()

        self.invoice_table = self._create_table(
            "invoice_table",
            ["ID", "INVOICE_NUMBER", "TYPE", "VENDOR", "AMOUNT", "DUE_DATE", "STATUS"],
        )
        self.invoice_table.cellDoubleClicked.connect(lambda _row, _col: self.open_selected_invoice_details())

        delete_button = QPushButton("Delete Selected Invoice", objectName="delete_invoice_button")
        delete_button.clicked.connect(self.delete_selected_invoice)

        layout.addWidget(form_group)
        layout.addLayout(filter_layout)
        layout.addWidget(self.invoice_table)
        layout.addWidget(QLabel("Tip: double-click an invoice row to open its details."))
        layout.addWidget(delete_button, alignment=Qt.AlignRight)

    def _build_posted_invoices_page(self):
        layout = QVBoxLayout(self.posted_invoices_page)
        group = QGroupBox("Posted Invoices", objectName="posted_invoices_group")
        group_layout = QVBoxLayout(group)

        self.posted_invoice_table = self._create_table(
            "posted_invoice_table",
            ["ID", "INVOICE_NUMBER", "TYPE", "VENDOR", "AMOUNT", "DUE_DATE", "STATUS"],
        )
        self.posted_invoice_table.cellDoubleClicked.connect(lambda _row, _col: self.open_selected_posted_invoice_details())
        group_layout.addWidget(self.posted_invoice_table)
        group_layout.addWidget(QLabel("Tip: double-click a posted invoice row to open its details."))

        delete_button = QPushButton("Delete Selected Posted Invoice", objectName="delete_posted_invoice_button")
        delete_button.clicked.connect(self.delete_selected_posted_invoice)

        layout.addWidget(group)
        layout.addWidget(delete_button, alignment=Qt.AlignRight)

    def _create_table(self, object_name: str, headers: list[str]) -> QTableWidget:
        table = QTableWidget(0, len(headers), objectName=object_name)
        table.setHorizontalHeaderLabels(headers)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setSelectionMode(QTableWidget.SingleSelection)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        return table

    def _refresh_vendor_dropdown(self):
        current_text = self.vendor_choice.currentText().strip() if hasattr(self, "vendor_choice") else ""
        self.vendor_choice.clear()
        self.vendor_choice.addItems([f"{v.id} - {v.name}" for v in self.vendors])
        if current_text:
            self.vendor_choice.setEditText(current_text)
        elif self.vendors:
            self.vendor_choice.setCurrentIndex(0)

    def add_vendor(self):
        name = self.vendor_name_entry.text().strip()
        email = self.vendor_email_entry.text().strip()
        phone = self.vendor_phone_entry.text().strip()

        if not name:
            QMessageBox.critical(self, "Validation", "Vendor name is required.")
            return

        vendor = Vendor(id=self.next_vendor_id, name=name, email=email, phone=phone)
        self.next_vendor_id += 1
        self.vendors.append(vendor)
        self._add_vendor_table_row(vendor)
        self._refresh_vendor_dropdown()

        self.vendor_name_entry.clear()
        self.vendor_email_entry.clear()
        self.vendor_phone_entry.clear()

    def _add_vendor_table_row(self, vendor: Vendor):
        row = self.vendor_table.rowCount()
        self.vendor_table.insertRow(row)
        self._set_table_row(self.vendor_table, row, [vendor.id, vendor.name, vendor.email, vendor.phone])

    def add_invoice(self):
        invoice_number = self.inv_num_entry.text().strip()
        invoice_type = self.inv_type.currentText().strip()
        vendor_display = self.vendor_choice.currentText().strip()
        amount_text = self.inv_amount_entry.text().strip()
        due_date = self.inv_due_entry.text().strip()
        notes = self.inv_notes_entry.text().strip()

        if not invoice_number:
            QMessageBox.critical(self, "Validation", "Invoice number is required.")
            return
        if not vendor_display:
            QMessageBox.critical(self, "Validation", "Vendor is required.")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            QMessageBox.critical(self, "Validation", "Amount must be a valid number.")
            return

        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            QMessageBox.critical(self, "Validation", "Due date must be in YYYY-MM-DD format.")
            return

        vendor_id = self._resolve_vendor_id(vendor_display)
        invoice = Invoice(
            id=self.next_invoice_id,
            invoice_number=invoice_number,
            invoice_type=invoice_type,
            vendor_id=vendor_id,
            amount=amount,
            due_date=due_date,
            notes=notes,
        )
        self.next_invoice_id += 1
        self.invoices.append(invoice)

        self.refresh_invoice_tables()
        self.inv_num_entry.clear()
        self.inv_amount_entry.clear()
        self.inv_notes_entry.clear()

    def _resolve_vendor_id(self, vendor_display: str) -> int:
        if " - " in vendor_display:
            vendor_id_part = vendor_display.split(" - ")[0]
            if vendor_id_part.isdigit():
                return int(vendor_id_part)

        matching_vendor = next((v for v in self.vendors if v.name.lower() == vendor_display.lower()), None)
        if matching_vendor:
            return matching_vendor.id

        vendor = Vendor(id=self.next_vendor_id, name=vendor_display, email="", phone="")
        self.next_vendor_id += 1
        self.vendors.append(vendor)
        self._add_vendor_table_row(vendor)
        self._refresh_vendor_dropdown()
        return vendor.id

    def _vendor_name(self, vendor_id: int) -> str:
        for vendor in self.vendors:
            if vendor.id == vendor_id:
                return vendor.name
        return "Unknown"

    def _selected_invoice_from_table(self, table: QTableWidget) -> Optional[Invoice]:
        selected_rows = table.selectionModel().selectedRows()
        if not selected_rows:
            return None
        invoice_id = int(table.item(selected_rows[0].row(), 0).text())
        return next((invoice for invoice in self.invoices if invoice.id == invoice_id), None)

    def _selected_invoice(self) -> Optional[Invoice]:
        return self._selected_invoice_from_table(self.invoice_table)

    def post_selected_invoice(self):
        invoice = self._selected_invoice()
        if not invoice:
            QMessageBox.critical(self, "Selection", "Select an invoice first.")
            return

        invoice.status = "Posted"
        self.refresh_invoice_tables()
        QMessageBox.information(self, "Success", f"Invoice {invoice.invoice_number} posted for payment processing.")

    def open_selected_invoice_details(self):
        invoice = self._selected_invoice()
        if invoice:
            self._show_invoice_details(invoice)

    def open_selected_posted_invoice_details(self):
        invoice = self._selected_invoice_from_table(self.posted_invoice_table)
        if invoice:
            self._show_invoice_details(invoice)

    def _show_invoice_details(self, invoice: Invoice):
        detail = QDialog(self)
        detail.setWindowTitle(f"Invoice Details - {invoice.invoice_number}")
        detail.setObjectName("invoice_detail_dialog")
        layout = QFormLayout(detail)

        rows = [
            ("Invoice ID", invoice.id),
            ("Invoice #", invoice.invoice_number),
            ("Type", invoice.invoice_type),
            ("Vendor", self._vendor_name(invoice.vendor_id)),
            ("Amount", f"{invoice.amount:.2f}"),
            ("Due Date", invoice.due_date),
            ("Status", invoice.status),
            ("Notes", invoice.notes or "(none)"),
        ]
        for label, value in rows:
            layout.addRow(f"{label}:", QLabel(str(value)))

        close_button = QPushButton("Close", objectName="invoice_detail_close_button")
        close_button.clicked.connect(detail.accept)
        layout.addRow(close_button)
        detail.exec()

    def filter_invoices(self):
        self.refresh_invoice_tables()

    def refresh_invoice_tables(self):
        selected_filter = self.invoice_filter.currentText().strip() if hasattr(self, "invoice_filter") else "All"
        self.invoice_table.setRowCount(0)
        self.posted_invoice_table.setRowCount(0)

        for invoice in self.invoices:
            if selected_filter == "All" or invoice.status == "Posted":
                self._add_invoice_table_row(self.invoice_table, invoice)
            if invoice.status == "Posted":
                self._add_invoice_table_row(self.posted_invoice_table, invoice)

    def _add_invoice_table_row(self, table: QTableWidget, invoice: Invoice):
        row = table.rowCount()
        table.insertRow(row)
        self._set_table_row(
            table,
            row,
            [
                invoice.id,
                invoice.invoice_number,
                invoice.invoice_type,
                self._vendor_name(invoice.vendor_id),
                f"{invoice.amount:.2f}",
                invoice.due_date,
                invoice.status,
            ],
        )

    def _set_table_row(self, table: QTableWidget, row: int, values: list[object]):
        for column, value in enumerate(values):
            item = QTableWidgetItem(str(value))
            item.setData(Qt.UserRole, value)
            table.setItem(row, column, item)

    def delete_selected_vendor(self):
        selected_rows = self.vendor_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.critical(self, "Selection", "Select a vendor first.")
            return

        vendor_id = int(self.vendor_table.item(selected_rows[0].row(), 0).text())
        self.vendors = [vendor for vendor in self.vendors if vendor.id != vendor_id]
        self.vendor_table.removeRow(selected_rows[0].row())
        self._refresh_vendor_dropdown()

    def delete_selected_invoice(self):
        invoice = self._selected_invoice()
        if not invoice:
            QMessageBox.critical(self, "Selection", "Select an invoice first.")
            return

        self.invoices = [item for item in self.invoices if item.id != invoice.id]
        self.refresh_invoice_tables()

    def delete_selected_posted_invoice(self):
        invoice = self._selected_invoice_from_table(self.posted_invoice_table)
        if not invoice:
            QMessageBox.critical(self, "Selection", "Select a posted invoice first.")
            return

        self.invoices = [item for item in self.invoices if item.id != invoice.id]
        self.refresh_invoice_tables()


def main():
    app = QApplication(sys.argv)
    window = ERPSuiteLiteApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
