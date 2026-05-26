import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


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
    invoice_type: str  # AP or AR
    vendor_id: int
    amount: float
    due_date: str
    notes: str
    status: str = "Draft"  # Draft or Posted


class ERPSuiteLiteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ERPSuite Lite")
        self.geometry("1100x700")

        self.vendors: list[Vendor] = []
        self.invoices: list[Invoice] = []
        self.next_vendor_id = 1
        self.next_invoice_id = 1

        self._build_login()

    def _build_login(self):
        self.login_frame = ttk.Frame(self, padding=20)
        self.login_frame.pack(fill="both", expand=True)

        card = ttk.LabelFrame(self.login_frame, text="Sign In", padding=20)
        card.pack(expand=True)

        ttk.Label(card, text="Username").grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = ttk.Entry(card, width=30)
        self.username_entry.grid(row=0, column=1, pady=5)

        ttk.Label(card, text="Password").grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(card, width=30, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        ttk.Button(card, text="Sign In", command=self.sign_in).grid(row=2, column=0, columnspan=2, pady=15)

        ttk.Label(card, text="(Any username/password is accepted)").grid(row=3, column=0, columnspan=2)

    def sign_in(self):
        self.login_frame.destroy()
        self._build_main_ui()

    def _build_main_ui(self):
        self.main_frame = ttk.Frame(self, padding=10)
        self.main_frame.pack(fill="both", expand=True)

        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(fill="both", expand=True)

        self.add_vendor_tab = ttk.Frame(notebook, padding=10)
        self.view_vendors_tab = ttk.Frame(notebook, padding=10)
        self.invoices_tab = ttk.Frame(notebook, padding=10)

        notebook.add(self.add_vendor_tab, text="Add Vendor")
        notebook.add(self.view_vendors_tab, text="View Vendors")
        notebook.add(self.invoices_tab, text="Invoices (AP / AR)")

        self._build_add_vendor_tab()
        self._build_view_vendors_tab()
        self._build_invoices_tab()

    def _build_add_vendor_tab(self):
        form = ttk.LabelFrame(self.add_vendor_tab, text="Add New Vendor", padding=10)
        form.pack(fill="x", padx=5, pady=5)

        ttk.Label(form, text="Name").grid(row=0, column=0, sticky="w")
        self.vendor_name_entry = ttk.Entry(form, width=30)
        self.vendor_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Email").grid(row=0, column=2, sticky="w")
        self.vendor_email_entry = ttk.Entry(form, width=30)
        self.vendor_email_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="Phone").grid(row=0, column=4, sticky="w")
        self.vendor_phone_entry = ttk.Entry(form, width=20)
        self.vendor_phone_entry.grid(row=0, column=5, padx=5, pady=5)

        ttk.Button(form, text="Add Vendor", command=self.add_vendor).grid(row=0, column=6, padx=10)

    def _build_view_vendors_tab(self):
        list_frame = ttk.LabelFrame(self.view_vendors_tab, text="Vendors", padding=10)
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        columns = ("id", "name", "email", "phone")
        self.vendor_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        for c in columns:
            self.vendor_tree.heading(c, text=c.upper())
            self.vendor_tree.column(c, width=160)
        self.vendor_tree.pack(fill="both", expand=True)

    def add_vendor(self):
        name = self.vendor_name_entry.get().strip()
        email = self.vendor_email_entry.get().strip()
        phone = self.vendor_phone_entry.get().strip()

        if not name:
            messagebox.showerror("Validation", "Vendor name is required.")
            return

        vendor = Vendor(id=self.next_vendor_id, name=name, email=email, phone=phone)
        self.next_vendor_id += 1
        self.vendors.append(vendor)

        self.vendor_tree.insert("", "end", values=(vendor.id, vendor.name, vendor.email, vendor.phone))
        self._refresh_vendor_dropdown()

        self.vendor_name_entry.delete(0, tk.END)
        self.vendor_email_entry.delete(0, tk.END)
        self.vendor_phone_entry.delete(0, tk.END)

    def _build_invoices_tab(self):
        form = ttk.LabelFrame(self.invoices_tab, text="Create Invoice", padding=10)
        form.pack(fill="x", padx=5, pady=5)

        ttk.Label(form, text="Invoice #").grid(row=0, column=0, sticky="w")
        self.inv_num_entry = ttk.Entry(form, width=20)
        self.inv_num_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Type").grid(row=0, column=2, sticky="w")
        self.inv_type = ttk.Combobox(form, values=["AP", "AR"], state="readonly", width=10)
        self.inv_type.set("AP")
        self.inv_type.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="Vendor").grid(row=0, column=4, sticky="w")
        self.vendor_choice = ttk.Combobox(form, values=[], state="readonly", width=25)
        self.vendor_choice.grid(row=0, column=5, padx=5, pady=5)

        ttk.Label(form, text="Amount").grid(row=1, column=0, sticky="w")
        self.inv_amount_entry = ttk.Entry(form, width=20)
        self.inv_amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form, text="Due Date (YYYY-MM-DD)").grid(row=1, column=2, sticky="w")
        self.inv_due_entry = ttk.Entry(form, width=15)
        self.inv_due_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))
        self.inv_due_entry.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(form, text="Notes").grid(row=1, column=4, sticky="w")
        self.inv_notes_entry = ttk.Entry(form, width=30)
        self.inv_notes_entry.grid(row=1, column=5, padx=5, pady=5)

        ttk.Button(form, text="Save Invoice", command=self.add_invoice).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(form, text="Post Selected Invoice", command=self.post_selected_invoice).grid(row=2, column=2, columnspan=2, pady=10)

        filter_frame = ttk.Frame(self.invoices_tab)
        filter_frame.pack(fill="x", padx=5, pady=5)
        ttk.Label(filter_frame, text="Invoice View:").pack(side="left")
        self.invoice_filter = ttk.Combobox(filter_frame, values=["All", "Posted"], state="readonly", width=12)
        self.invoice_filter.set("All")
        self.invoice_filter.pack(side="left", padx=8)
        self.invoice_filter.bind("<<ComboboxSelected>>", self.filter_invoices)

        list_frame = ttk.LabelFrame(self.invoices_tab, text="Invoices", padding=10)
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        columns = ("id", "invoice_number", "type", "vendor", "amount", "due_date", "status")
        self.invoice_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        for c in columns:
            self.invoice_tree.heading(c, text=c.upper())
            self.invoice_tree.column(c, width=130)
        self.invoice_tree.pack(fill="both", expand=True)
        self.invoice_tree.bind("<ButtonRelease-1>", self.open_selected_invoice_details)
        self.invoice_tree.bind("<Double-1>", self.open_selected_invoice_details)

        ttk.Label(list_frame, text="Tip: double-click an invoice row to open its details.").pack(anchor="w", pady=5)

    def _refresh_vendor_dropdown(self):
        vendor_labels = [f"{v.id} - {v.name}" for v in self.vendors]
        self.vendor_choice["values"] = vendor_labels
        if vendor_labels and not self.vendor_choice.get():
            self.vendor_choice.set(vendor_labels[0])

    def add_invoice(self):
        if not self.vendors:
            messagebox.showerror("Validation", "Please add a vendor first.")
            return

        invoice_number = self.inv_num_entry.get().strip()
        invoice_type = self.inv_type.get().strip()
        vendor_display = self.vendor_choice.get().strip()
        amount_text = self.inv_amount_entry.get().strip()
        due_date = self.inv_due_entry.get().strip()
        notes = self.inv_notes_entry.get().strip()

        if not invoice_number:
            messagebox.showerror("Validation", "Invoice number is required.")
            return

        if not vendor_display:
            messagebox.showerror("Validation", "Vendor is required.")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            messagebox.showerror("Validation", "Amount must be a valid number.")
            return

        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Validation", "Due date must be in YYYY-MM-DD format.")
            return

        vendor_id = int(vendor_display.split(" - ")[0])
        vendor_name = self._vendor_name(vendor_id)

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

        self.invoice_tree.insert(
            "",
            "end",
            iid=str(invoice.id),
            values=(invoice.id, invoice.invoice_number, invoice.invoice_type, vendor_name, f"{invoice.amount:.2f}", invoice.due_date, invoice.status),
        )
        self.filter_invoices()

        self.inv_num_entry.delete(0, tk.END)
        self.inv_amount_entry.delete(0, tk.END)
        self.inv_notes_entry.delete(0, tk.END)

    def _vendor_name(self, vendor_id: int) -> str:
        for v in self.vendors:
            if v.id == vendor_id:
                return v.name
        return "Unknown"

    def _selected_invoice(self) -> Optional[Invoice]:
        selected = self.invoice_tree.selection()
        if not selected:
            return None
        invoice_id = int(selected[0])
        for inv in self.invoices:
            if inv.id == invoice_id:
                return inv
        return None

    def post_selected_invoice(self):
        invoice = self._selected_invoice()
        if not invoice:
            messagebox.showerror("Selection", "Select an invoice first.")
            return

        invoice.status = "Posted"
        self.invoice_tree.item(str(invoice.id), values=(
            invoice.id,
            invoice.invoice_number,
            invoice.invoice_type,
            self._vendor_name(invoice.vendor_id),
            f"{invoice.amount:.2f}",
            invoice.due_date,
            invoice.status,
        ))
        self.filter_invoices()
        messagebox.showinfo("Success", f"Invoice {invoice.invoice_number} posted for payment processing.")

    def open_selected_invoice_details(self, _event=None):
        invoice = self._selected_invoice()
        if not invoice:
            return

        detail = tk.Toplevel(self)
        detail.title(f"Invoice Details - {invoice.invoice_number}")
        detail.geometry("450x350")

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

        container = ttk.Frame(detail, padding=15)
        container.pack(fill="both", expand=True)

        for i, (label, value) in enumerate(rows):
            ttk.Label(container, text=f"{label}:", font=("TkDefaultFont", 10, "bold")).grid(row=i, column=0, sticky="nw", pady=4)
            ttk.Label(container, text=str(value), wraplength=260).grid(row=i, column=1, sticky="nw", pady=4)

    def filter_invoices(self, _event=None):
        selected_filter = self.invoice_filter.get().strip() if hasattr(self, "invoice_filter") else "All"
        for inv in self.invoices:
            visible = selected_filter == "All" or inv.status == "Posted"
            if self.invoice_tree.exists(str(inv.id)):
                if visible:
                    self.invoice_tree.reattach(str(inv.id), "", "end")
                else:
                    self.invoice_tree.detach(str(inv.id))


if __name__ == "__main__":
    app = ERPSuiteLiteApp()
    app.mainloop()
