import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector

# ---------------- Database Connection ----------------
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="atulmehta12345@",   # change if needed
            database="retail_inventory"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("DB Error", f"Cannot connect: {err}")
        return None


# ---------------- Fetch and Show Table ----------------
def show_table(table_name):
    for w in table_frame.winfo_children():
        w.destroy()

    con = connect_db()
    if not con:
        return
    cur = con.cursor()

    # Get column names
    cur.execute(f"SHOW COLUMNS FROM {table_name}")
    cols = [c[0] for c in cur.fetchall()]

    # Create table view
    tree = ttk.Treeview(table_frame, columns=cols, show="headings")
    vsb = ttk.Scrollbar(table_frame, command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    # Fetch and insert rows
    cur.execute(f"SELECT * FROM {table_name}")
    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)

    tree.pack(fill=tk.BOTH, expand=True)
    con.close()


# ---------------- Product Operations ----------------
def add_product():
    con = connect_db()
    if not con:
        return
    name = simpledialog.askstring("Product", "Enter product name:")
    price = simpledialog.askfloat("Price", "Enter price:")
    qty = simpledialog.askinteger("Quantity", "Enter quantity:")
    supplier = simpledialog.askinteger("Supplier ID", "Enter supplier ID:")

    if not all([name, price, qty, supplier]):
        messagebox.showwarning("Input Error", "All fields required.")
        return

    cur = con.cursor()
    cur.execute("INSERT INTO products (product_name, price, quantity, supplier_id) VALUES (%s, %s, %s, %s)",
                (name, price, qty, supplier))
    con.commit()
    con.close()
    messagebox.showinfo("Done", "Product added!")
    show_table("products")


def update_product_price():
    con = connect_db()
    if not con:
        return
    pid = simpledialog.askinteger("Product ID", "Enter product ID:")
    new_price = simpledialog.askfloat("Price", "Enter new price:")
    if not pid or not new_price:
        messagebox.showwarning("Input Error", "Both fields required.")
        return

    cur = con.cursor()
    cur.execute("UPDATE products SET price=%s WHERE product_id=%s", (new_price, pid))
    con.commit()
    con.close()
    messagebox.showinfo("Done", "Price updated!")
    show_table("products")


def delete_product():
    con = connect_db()
    if not con:
        return
    pid = simpledialog.askinteger("Product ID", "Enter product ID:")
    if not pid:
        messagebox.showwarning("Input Error", "Product ID required.")
        return

    cur = con.cursor()
    cur.execute("DELETE FROM products WHERE product_id=%s", (pid,))
    con.commit()
    con.close()
    messagebox.showinfo("Done", "Product deleted!")
    show_table("products")


# ---------------- Customer Operations ----------------
def add_customer():
    con = connect_db()
    if not con:
        return
    name = simpledialog.askstring("Customer", "Enter customer name:")
    phone = simpledialog.askstring("Phone", "Enter phone number:")
    if not name or not phone:
        messagebox.showwarning("Input Error", "All fields required.")
        return

    cur = con.cursor()
    cur.execute("INSERT INTO customers (customer_name, phone) VALUES (%s, %s)", (name, phone))
    con.commit()
    con.close()
    messagebox.showinfo("Done", "Customer added!")
    show_table("customers")


# ---------------- UI Setup ----------------
root = tk.Tk()
root.title("🛒 Retail Inventory System")
root.geometry("950x600")

# Header
tk.Label(root, text="Retail Inventory Dashboard", bg="#2E86C1",
         fg="white", font=("Arial", 18, "bold"), pady=10).pack(fill=tk.X)

# Table Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

for tbl in ["suppliers", "products", "customers", "sales", "sale_items"]:
    tk.Button(btn_frame, text=tbl.capitalize(), width=13, bg="#3498DB", fg="white",
              command=lambda t=tbl: show_table(t)).pack(side=tk.LEFT, padx=5)

# Action Buttons
action_frame = tk.Frame(root)
action_frame.pack(pady=10)

actions = [
    ("➕ Add Product", "#27AE60", add_product),
    ("💲 Update Price", "#F39C12", update_product_price),
    ("❌ Delete Product", "#E74C3C", delete_product),
    ("👤 Add Customer", "#9B59B6", add_customer)
]

for text, color, cmd in actions:
    tk.Button(action_frame, text=text, bg=color, fg="white",
              width=15, font=("Arial", 11, "bold"), command=cmd).pack(side=tk.LEFT, padx=5)

# Data Display
table_frame = tk.Frame(root, bg="white", relief=tk.RIDGE, borderwidth=2)
table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

# Exit Button
tk.Button(root, text="Exit", command=root.quit, bg="#E74C3C", fg="white",
          width=10, font=("Arial", 11, "bold")).pack(pady=10)

root.mainloop()
