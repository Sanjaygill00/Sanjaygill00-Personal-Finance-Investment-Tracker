import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import ttkbootstrap as tb  # Import ttkbootstrap for better UI
import matplotlib.pyplot as plt  # Import for pie chart visualization

# Database Setup
conn = sqlite3.connect("finance.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    category TEXT,
    amount REAL,
    description TEXT
)
''')
conn.commit()

def add_transaction(type, category, amount, description):
    try:
        amount = float(amount)
        cursor.execute("INSERT INTO transactions (type, category, amount, description) VALUES (?, ?, ?, ?)",
                       (type, category, amount, description))
        conn.commit()
        reset_id_sequence()
        refresh_table()
        messagebox.showinfo("Success", f"{type} added successfully!")
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number!")

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM transactions")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def delete_transaction():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a record to delete!")
        return
    item = tree.item(selected_item)
    cursor.execute("DELETE FROM transactions WHERE id=?", (item['values'][0],))
    conn.commit()
    reset_id_sequence()
    refresh_table()

def delete_all_transactions():
    if messagebox.askyesno("Warning", "Are you sure you want to delete all data?"):
        cursor.execute("DELETE FROM transactions")
        conn.commit()
        reset_id_sequence()
        refresh_table()
        messagebox.showinfo("Success", "All data deleted successfully!")

def reset_id_sequence():
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='transactions'")
    conn.commit()

def show_expense_tracker():
    expenses_window = tb.Toplevel(root)
    expenses_window.title("Expense Tracker")
    expenses_window.geometry("400x300")
    tb.Label(expenses_window, text="Expense Breakdown", font=("Arial", 14, "bold"), bootstyle="primary").pack(pady=10)
    
    cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE type='Expense' GROUP BY category")
    expenses = cursor.fetchall()
    
    total_expense = 0
    for category, amount in expenses:
        total_expense += amount
        tb.Label(expenses_window, text=f"{category}: {amount}", font=("Arial", 12)).pack()
    
    tb.Label(expenses_window, text=f"Total Expenses: {total_expense}", font=("Arial", 14, "bold"), foreground="red").pack(pady=10)

def show_income_tracker():
    income_window = tb.Toplevel(root)
    income_window.title("Income Tracker")
    income_window.geometry("400x300")
    tb.Label(income_window, text="Income Sources", font=("Arial", 14, "bold"), bootstyle="primary").pack(pady=10)
    
    cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE type='Income' GROUP BY category")
    income = cursor.fetchall()
    
    total_income = 0
    for category, amount in income:
        total_income += amount
        tb.Label(income_window, text=f"{category}: {amount}", font=("Arial", 12)).pack()
    
    tb.Label(income_window, text=f"Total Income: {total_income}", font=("Arial", 14, "bold"), foreground="green").pack(pady=10)

def sip_calculator():
    sip_window = tb.Toplevel(root)
    sip_window.title("SIP Calculator")
    sip_window.geometry("400x600")
    tb.Label(sip_window, text="SIP Calculator", font=("Arial", 14, "bold"), bootstyle="primary").pack(pady=10)

    # Input fields for SIP calculation
    tb.Label(sip_window, text="Monthly Investment (₹):", font=("Arial", 12)).pack(pady=5)
    monthly_investment = tb.Entry(sip_window, font=("Arial", 12))
    monthly_investment.pack(pady=5)

    tb.Label(sip_window, text="Annual Interest Rate (%):", font=("Arial", 12)).pack(pady=5)
    annual_rate = tb.Entry(sip_window, font=("Arial", 12))
    annual_rate.pack(pady=5)

    tb.Label(sip_window, text="Investment Period (Years):", font=("Arial", 12)).pack(pady=5)
    period = tb.Entry(sip_window, font=("Arial", 12))
    period.pack(pady=5)

    '''
    def calculate_sip():
        try:
            p = float(monthly_investment.get())
            r = float(annual_rate.get()) / 100 / 12
            n = int(period.get()) * 12
            future_value = p * ((1 + r)**n - 1) * (1 + r) / r
            tb.Label(sip_window, text=f"Future Value: ₹{future_value:,.2f}", font=("Arial", 14, "bold"), foreground="green").pack(pady=10)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")

    tb.Button(sip_window, text="Calculate", command=calculate_sip, bootstyle="success").pack(pady=10)
    '''
    def sip_calculator():
        sip_window = tb.Toplevel(root)
        sip_window.title("SIP Calculator")
        sip_window.geometry("400x400")
        tb.Label(sip_window, text="SIP Calculator", font=("Arial", 14, "bold"), bootstyle="primary").pack(pady=10)

        # Input fields for SIP calculation
        tb.Label(sip_window, text="Monthly Investment (₹):", font=("Arial", 12)).pack(pady=5)
        monthly_investment = tb.Entry(sip_window, font=("Arial", 12))
        monthly_investment.pack(pady=5)

        tb.Label(sip_window, text="Annual Interest Rate (%):", font=("Arial", 12)).pack(pady=5)
        annual_rate = tb.Entry(sip_window, font=("Arial", 12))
        annual_rate.pack(pady=5)

        tb.Label(sip_window, text="Investment Period (Years):", font=("Arial", 12)).pack(pady=5)
        period = tb.Entry(sip_window, font=("Arial", 12))
        period.pack(pady=5)

    def calculate_sip():
        try:
            # Gather and process input values
            p = float(monthly_investment.get())
            r = float(annual_rate.get()) / 100 / 12
            n = int(period.get()) * 12
            
            # Calculate future value
            future_value = p * ((1 + r)**n - 1) * (1 + r) / r
            total_investment = p * n
            profit = future_value - total_investment

            # Display investment details
            tb.Label(sip_window, text=f"Total Investment: ₹{total_investment:,.2f}", font=("Arial", 12), foreground="blue").pack(pady=5)
            tb.Label(sip_window, text=f"Profit Earned: ₹{profit:,.2f}", font=("Arial", 12), foreground="green").pack(pady=5)
            tb.Label(sip_window, text=f"Future Value: ₹{future_value:,.2f}", font=("Arial", 14, "bold"), foreground="purple").pack(pady=10)

            # Create Pie Chart
            def show_pie_chart():
                labels = ['Total Investment', 'Profit']
                sizes = [total_investment, profit]
                colors = ['#FFA07A', '#90EE90']
                explode = (0, 0.1)  # Highlight profit slice

                plt.figure(figsize=(6, 6))
                plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
                plt.title("Investment Breakdown")
                plt.show()

            # Add "Show Pie Chart" button
            tb.Button(sip_window, text="Show Pie Chart", command=show_pie_chart, bootstyle="info").pack(pady=5)

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")

    # Add "Calculate" button
    tb.Button(sip_window, text="Calculate", command=calculate_sip, bootstyle="success").pack(pady=10)

root = tb.Window(themename="superhero")  # Use ttkbootstrap theme
root.title("Finance Tracker")
root.geometry("700x600")

navbar = tb.Label(root, text="Personal Finance & Investment Tracker", font=("Arial", 16, "bold"), bootstyle="inverse-primary", padding=10)
navbar.pack(fill="x")

frame = tb.Frame(root, padding=10)
frame.pack(pady=10)

tb.Label(frame, text="Category", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
category = tk.StringVar()
category_dropdown = tb.Combobox(frame, textvariable=category, values=["Food", "Transport", "Entertainment", "Bills", "Salary", "Other"], font=("Arial", 12))
category_dropdown.grid(row=0, column=1, padx=10, pady=5)
category_dropdown.set("Food")

tb.Label(frame, text="Amount", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
amount_entry = tb.Entry(frame, font=("Arial", 12))
amount_entry.grid(row=1, column=1, padx=10, pady=5)

tb.Label(frame, text="Description", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
desc_entry = tb.Entry(frame, font=("Arial", 12))
desc_entry.grid(row=2, column=1, padx=10, pady=5)

button_frame = tb.Frame(root, padding=10)
button_frame.pack()

tb.Button(button_frame, text="Add Expense", command=lambda: add_transaction("Expense", category.get(), amount_entry.get(), desc_entry.get()), bootstyle="danger").grid(row=0, column=0, padx=10, pady=5)
tb.Button(button_frame, text="Add Income", command=lambda: add_transaction("Income", category.get(), amount_entry.get(), desc_entry.get()), bootstyle="success").grid(row=0, column=1, padx=10, pady=5)
tb.Button(button_frame, text="Delete Selected", command=delete_transaction, bootstyle="warning").grid(row=1, column=0, padx=10, pady=5)
tb.Button(button_frame, text="Delete All Data", command=delete_all_transactions, bootstyle="secondary").grid(row=1, column=1, padx=10, pady=5)
tb.Button(button_frame, text="Expense Tracker", command=show_expense_tracker, bootstyle="info").grid(row=2, column=0, padx=10, pady=5)
tb.Button(button_frame, text="Income Tracker", command=show_income_tracker, bootstyle="info").grid(row=2, column=1, padx=10, pady=5)
tb.Button(button_frame, text="SIP Calculator", command=sip_calculator, bootstyle="info").grid(row=3, column=0, padx=10, pady=5)

tree = ttk.Treeview(root, columns=("ID", "Type", "Category", "Amount", "Description"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Type", text="Type")
tree.heading("Category", text="Category")
tree.heading("Amount", text="Amount")
tree.heading("Description", text="Description")
tree.pack(pady=10)

refresh_table()
root.mainloop()

conn.close()
